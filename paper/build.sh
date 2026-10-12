#!/usr/bin/env bash
# Build the distributable paper. Word (.docx) is the distribution format; draft.md is the editable source.
# The .docx gets math as plain Unicode (portable across Word, Google Docs, LibreOffice); main.tex keeps LaTeX math.
set -euo pipefail
cd "$(dirname "$0")"
python3 tex2unicode.py draft.md > .draft_unicode.md
pandoc .draft_unicode.md --resource-path=.:.. -o cold_fusion_gap_preprint.docx
rm -f .draft_unicode.md
pandoc draft.md -s -o main.tex
echo "built cold_fusion_gap_preprint.docx and main.tex"
