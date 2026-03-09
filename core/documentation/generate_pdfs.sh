#!/usr/bin/env bash
set -euo pipefail

DOC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

COMMON_ARGS=(
  --from markdown
  --to pdf
  --pdf-engine=xelatex
  --standalone
  --wrap=preserve
  --syntax-highlighting=tango
  -V papersize:a4
  -V geometry:margin=1in
  -V fontsize=11pt
  -V linestretch=1.15
  -V colorlinks
  -V linkcolor=blue
  -V urlcolor=blue
  -V toccolor=black
  -V monofont=Menlo
)

for md_file in "$DOC_DIR"/*.md; do
  [[ -f "$md_file" ]] || continue
  if [[ "$(basename "$md_file")" == "business_email_draft.md" ]]; then
    continue
  fi
  pdf_file="${md_file%.md}.pdf"

  pandoc \
    "${COMMON_ARGS[@]}" \
    "$md_file" \
    -o "$pdf_file"

  echo "Generated $pdf_file"
done
