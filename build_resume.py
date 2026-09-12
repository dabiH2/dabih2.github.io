#!/usr/bin/env python3
"""
build_resume.py  --  builds and gate-checks the published CV for dabih2.github.io.

    python build_resume.py            # build + gate-check, do not publish on failure
    python build_resume.py --no-gate  # build only (not recommended)

Source of truth is resume/resume_gdesimini_published.tex. The compiled PDF is placed
at the repo root as Gabriele_Desimini_Resume.pdf, which is what the site links to.

THE GATE IS THE POINT. Before 2026-09-12 this PDF was uploaded by hand with no check,
and it sat on a public page for 23 days carrying a retired phone number. The build now
refuses to overwrite the published PDF if the source trips any pattern in
../Applications/07-automation/daily/gate_tokens.txt. Market is "published", which is the
one market that tolerates both phone numbers, because this document deliberately carries
the EU number and the North America number together.

If the gate list cannot be found, the build fails. That is deliberate: silently passing
because the list is missing is the exact failure this replaces.
"""
import os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "resume", "resume_gdesimini_published.tex")
PAGE = os.path.join(HERE, "index.html")  # the site itself is an outbound artefact too
OUT = os.path.join(HERE, "Gabriele_Desimini_Resume.pdf")
APPS = os.path.normpath(os.path.join(HERE, os.pardir, "Applications"))
BUILD = os.path.join(HERE, "resume", "_build")


def gate(path, market="published"):
    sys.path.insert(0, os.path.join(APPS, "03-components"))
    try:
        import assemble
    except Exception as exc:
        print("GATE UNAVAILABLE: cannot import assemble.py from %s (%s)" % (APPS, exc))
        return ["gate unavailable"]
    return assemble.check(path, market=market)


def main():
    if not os.path.exists(SRC):
        sys.exit("missing source: %s" % SRC)
    os.makedirs(BUILD, exist_ok=True)

    if "--no-gate" not in sys.argv:
        failed = False
        # Both the PDF source and index.html are checked. The page carried an
        # unscoped "No sponsorship needed" chip until 2026-09-12; a gate that only
        # looks at the PDF would never have seen it.
        for label, target, mkt in (("resume source", SRC, "published"),
                                   ("index.html", PAGE, "html")):
            if not os.path.exists(target):
                continue
            found = gate(target, mkt)
            probs = [x for x in found if not x.startswith("REVIEW ")]
            review = [x for x in found if x.startswith("REVIEW ")]
            for x in review:
                print("gate %s: %s" % (label, x))
            if probs:
                failed = True
                print("GATE FAILED on %s:" % label)
                for x in probs:
                    print("   %s" % x)
        if failed:
            print("nothing published.")
            sys.exit(1)
        print("gate: OK (resume source and index.html)")

    for i in (1, 2):  # twice, so \hfill and page refs settle
        r = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
             "-output-directory", BUILD, SRC],
            capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout[-3000:])
            sys.exit("pdflatex failed on pass %d" % i)

    built = os.path.join(BUILD, "resume_gdesimini_published.pdf")
    if not os.path.exists(built):
        sys.exit("no PDF produced")
    shutil.copy2(built, OUT)
    size = os.path.getsize(OUT)
    print("published: %s (%d bytes)" % (os.path.basename(OUT), size))
    print("now: git add -A && git commit && git push")


if __name__ == "__main__":
    main()
