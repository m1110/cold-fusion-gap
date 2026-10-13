#!/usr/bin/env bash
# Build the distributable note (.docx). Math is converted to portable text by the shared paper/tex2unicode.py.
set -euo pipefail
cd "$(dirname "$0")"
python3 ../../paper/tex2unicode.py note.md > .note_unicode.md
pandoc .note_unicode.md --resource-path=. -o other_paths_note.docx
rm -f .note_unicode.md
echo "built other_paths_note.docx"
