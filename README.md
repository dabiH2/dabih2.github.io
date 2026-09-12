# gabriele desimini

AI/ML Software Engineer. Portfolio site, live at **https://dabih2.github.io**

Single self-contained HTML file. No build step, no dependencies, no external requests,
no trackers, no cookies. Open `index.html` in any browser and it works offline.

| File | What it is |
|---|---|
| `index.html` | The site. Inline CSS and JS, light and dark themes, WCAG AA contrast throughout. |
| `Gabriele_Desimini_Resume.pdf` | Resume, linked from three places on the page. **Built, not uploaded. See below.** |
| `resume/resume_gdesimini_published.tex` | Source of truth for the resume PDF. |
| `build_resume.py` | Compiles and gate-checks the resume, then replaces the published PDF. |

Contact: [dabi.ai.eng@gmail.com](mailto:dabi.ai.eng@gmail.com) | [LinkedIn](https://linkedin.com/in/gabriele-desimini)

## Updating the resume

The PDF is **built, not uploaded**. Edit the source, then:

```
python build_resume.py
git add -A && git commit -m "Update resume" && git push
```

`build_resume.py` compiles with `pdflatex` (A4, 2 pages) and, before it overwrites
`Gabriele_Desimini_Resume.pdf`, checks the source against
`../Applications/07-automation/daily/gate_tokens.txt` under market `published`.
If any retired claim is present, the build stops and publishes nothing. If the gate
list cannot be read, the build also stops, because silently passing is the failure
this replaces.

Retiring a future claim is a one-line edit to `gate_tokens.txt`. Nothing else changes.

**Why this exists.** Until 2026-09-12 this PDF was uploaded by hand with no check. It
carried a phone number that had been retired on 2026-08-20, stayed on a public page for
23 days, and was linked from live job applications, including one that reached an
interview. A build that can fail is cheaper than a page nobody rechecks.

`resume/Gabriele_Desimini_Resume_PREVIOUS_20260912.pdf` is the last hand-uploaded version,
kept for reference.
