# Conventions for this repository

- **Papers are distributed as Word (.docx).** Every paper (preprint, write-up, note intended for distribution) starts with a `.docx` deliverable. Keep an editable Markdown source next to it and build with the paper's `build.sh` (pandoc). `paper/tex2unicode.py` converts inline LaTeX math to portable Unicode / Word sub- and superscripts so the .docx reads the same in Word, Google Docs and LibreOffice. The LaTeX (`main.tex`) is a secondary output for arXiv.
- Render every .docx to PDF and look at it before committing (LibreOffice: `soffice --headless --convert-to pdf`, then `pdftoppm`).
- Notebooks: build from a script, execute with `jupyter nbconvert --execute --inplace`, and write conclusions only after reading the computed output. Numbers in prose must match the printed results.
- `notebooks/cfsolve.py` is the shared, validated solver. Keep `python -m pytest tests` passing.
- Inputs that are recalled, secondary or unverified are marked as such (see VERIFICATION.md).
- Fetch literature only with `tools/fetch.py` (official APIs, rate-limited, cached). Never automate Google Scholar or PhilPapers.
