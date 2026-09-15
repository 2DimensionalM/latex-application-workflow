# Build workflow

Build targets are declared in `scripts/build-targets.json`. The job name is always the LaTeX entry filename stem.

Builds use a fresh temporary auxiliary directory and write review PDFs under ignored `output/review/`. Review page count, whitespace, clipping, and LaTeX warnings before using a document externally.

Do not publish or commit generated PDFs from this skeleton.

