# 求职进展（按岗位）

本文件维护两张表：**（1）岗位总表（当前快照）** = 一行对应 `targets/<slug>/` 下一个真实岗位包；**（2）历史动作（带日期）** = 真实求职事件时间线（投递、面试、补材料、结果等），按日期倒序排列（最新在最上）。

与仓库 `targets/<slug>/metadata.yaml` 的联动约束、行分组排序规则、编号规则及更新流程，详见 **`.agent/rules/status.md`** 与 Skill **`.agent/skills/status-and-publish/SKILL.md`**。

---

## 「进展」列标准用语（与 `metadata.yaml` 的 `status` 映射）

| 准备（`draft` / `open`） | 写材料（`draft` / `open`） | 审核与待投（`draft` / `open`） | 投递与流程（`applied` / `interviewing`） | 结果与终态（`offer` / `rejected` / `closed`） |
|---|---|---|---|---|
| 待核实 / Pending Verification | 写简历 / Drafting Resume | 审核简历 / Reviewing Resume | 已投递 / Applied | 已拿 offer / Offer |
| 待预写 / Pending Pre-write | 写求职信 / Drafting Letter | 审核求职信 / Reviewing Letter | 一面 / 二面 / 终面 / Interview | 已拒 / Rejected |
| | | 待投递 / Ready to Apply | 补材料 / Follow-up Docs | 已下架 / Closed |

---

## 岗位总表（当前快照）

| 编号 | 公司 | 岗位 | 地点 | 招聘页 | JD | 进展 | 简历 | 求职信 |
|------|------|------|--------|--------|-----|------|----------|------------|

---

## 历史动作（带日期）

| 日期 | 公司 | 岗位（或编号） | 动作 |
|------|------|----------------|------|

---

## 新行模板（复制或通过 `workspace.py init` 自动插入）

**岗位总表（9 列）：**

```markdown
| 001 | Example Corp | Data & AI Engineer Intern（REQ-1001） | Amsterdam, Netherlands | [链接](https://example.com/jobs/1001) | [JD](targets/example-corp-data-ai-intern-amsterdam/jd.md) | 待预写 | — | — |
```

**历史动作（4 列，插在「历史动作」表头下一行）：**

```markdown
| 2026-11-03 | Example Corp | 001（REQ-1001，Data & AI Engineer Intern） | 已投递 |
```
