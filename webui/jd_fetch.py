"""Fetch a job description server-side so the Claude run does not have to.

Supports LinkedIn job links (public guest API), Workday (*.myworkdayjobs.com, public cxs API)
and any page that embeds schema.org JobPosting JSON-LD. Returns None when nothing usable is found;
the Claude run then falls back to its own WebFetch.
"""
from __future__ import annotations

from html.parser import HTMLParser
import html
import json
import re
from urllib.parse import parse_qs, urlparse
import urllib.request

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
BLOCK_TAGS = {"p", "div", "br", "li", "ul", "ol", "h1", "h2", "h3", "h4", "tr"}


def get(url: str, data: bytes | None = None, kind: str = "text/html") -> str:
    headers = {"User-Agent": UA, "Accept-Language": "en", "Accept": kind}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8", "replace")


class _Text(HTMLParser):
    """Plain text of the whole fragment, or only of the first element carrying `cls`."""

    def __init__(self, cls: str | None = None):
        super().__init__()
        self.cls, self.depth, self.parts = cls, 0 if cls else 1, []

    def handle_starttag(self, tag, attrs):
        if self.depth:
            if tag not in ("br",):
                self.depth += 1
            if tag in BLOCK_TAGS:
                self.parts.append("\n- " if tag == "li" else "\n")
        elif self.cls and self.cls in (dict(attrs).get("class") or "").split():
            self.depth = 1

    def handle_endtag(self, tag):
        if self.depth and tag != "br":
            self.depth -= 1
            if tag in BLOCK_TAGS:
                self.parts.append("\n")
            if self.cls and self.depth == 0:
                self.cls = "__done__"

    def handle_data(self, data):
        if self.depth:
            self.parts.append(data)

    def text(self) -> str:
        lines = [re.sub(r"[ \t\xa0]+", " ", l).strip() for l in "".join(self.parts).splitlines()]
        return re.sub(r"\n{3,}", "\n\n", "\n".join(l for l in lines if l.strip() not in ("", "-"))).strip()


def text_of(fragment: str, cls: str | None = None) -> str:
    parser = _Text(cls)
    parser.feed(fragment)
    return parser.text()


def linkedin(url: str) -> dict | None:
    u = urlparse(url)
    job_id = (re.search(r"/jobs/view/(?:[^/]*-)?(\d{6,})", u.path) or [None, None])[1] \
        or (parse_qs(u.query).get("currentJobId") or [None])[0]
    if not job_id:
        return None
    page = get(f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}")
    field = lambda cls: text_of(page, cls).replace("\n", " ").strip()
    description = text_of(page, "show-more-less-html__markup")
    if not description:
        return None
    criteria = re.findall(
        r'description__job-criteria-subheader">\s*(.*?)\s*</h3>.*?description__job-criteria-text[^>]*>\s*(.*?)\s*</span>',
        page, re.S)
    return {
        "title": field("top-card-layout__title"),
        "company": field("topcard__org-name-link"),
        "location": field("topcard__flavor--bullet"),
        "source": f"https://www.linkedin.com/jobs/view/{job_id}/",
        "facts": {html.unescape(k): html.unescape(v) for k, v in criteria},
        "description": description,
    }


def workday(url: str) -> dict | None:
    u = urlparse(url)
    if not u.netloc.endswith(".myworkdayjobs.com") or "/job/" not in u.path:
        return None
    tenant = u.netloc.split(".")[0]
    before, after = u.path.split("/job/", 1)
    site = [p for p in before.split("/") if p and not re.fullmatch(r"[a-z]{2}-[A-Z]{2}", p)][-1]
    info = json.loads(get(f"https://{u.netloc}/wday/cxs/{tenant}/{site}/job/{after}", kind="application/json"))
    job = info.get("jobPostingInfo") or {}
    if not job.get("jobDescription"):
        return None
    return {
        "title": job.get("title", ""),
        "company": (info.get("hiringOrganization") or {}).get("name", "") or tenant,
        "location": job.get("location", ""),
        "source": job.get("externalUrl") or url,
        "facts": {k: str(job[k]) for k in ("jobReqId", "timeType", "postedOn", "startDate", "canApply") if job.get(k) not in (None, "")},
        "description": text_of(job["jobDescription"]),
    }


def json_ld(url: str) -> dict | None:
    page = get(url)
    for block in re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', page, re.S | re.I):
        try:
            data = json.loads(block)
        except ValueError:
            continue
        for item in data if isinstance(data, list) else data.get("@graph", [data]):
            if isinstance(item, dict) and item.get("@type") == "JobPosting" and item.get("description"):
                org = item.get("hiringOrganization") or {}
                loc = item.get("jobLocation") or {}
                loc = loc[0] if isinstance(loc, list) and loc else loc
                addr = (loc.get("address") or {}) if isinstance(loc, dict) else {}
                place = ", ".join(x for x in (addr.get("addressLocality"), addr.get("addressCountry")) if isinstance(x, str))
                return {
                    "title": item.get("title", ""),
                    "company": org.get("name", "") if isinstance(org, dict) else str(org),
                    "location": place,
                    "source": url,
                    "facts": {k: str(item[k]) for k in ("datePosted", "validThrough", "employmentType", "identifier") if item.get(k)},
                    "description": text_of(item["description"]),
                }
    return None


def fetch(url: str) -> dict | None:
    host = urlparse(url).netloc
    handlers = [linkedin] if "linkedin.com" in host else [workday] if host.endswith(".myworkdayjobs.com") else []
    for handler in handlers + [json_ld]:
        try:
            found = handler(url)
        except (OSError, ValueError, KeyError, IndexError):
            found = None
        if found and len(found["description"]) > 200:
            return found
    return None


def as_text(jd: dict) -> str:
    facts = "".join(f"- {k}: {v}\n" for k, v in jd.get("facts", {}).items())
    return (f"Title: {jd['title']}\nCompany: {jd['company']}\nLocation: {jd['location']}\nSource: {jd['source']}\n"
            f"{facts}\n{jd['description']}")
