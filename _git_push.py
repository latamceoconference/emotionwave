# -*- coding: utf-8 -*-
"""Run git from repo root without embedding Unicode paths in shell."""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))


def git(*args):
    return subprocess.run(
        ["git", "-C", ROOT, *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def main():
    r = git("status", "-sb")
    print(r.stdout.strip())
    if r.returncode != 0:
        print(r.stderr, file=sys.stderr)
        return r.returncode

    r = git("diff", "--stat")
    if r.stdout.strip():
        print(r.stdout)

    r = git("add", "-A")
    if r.returncode != 0:
        print(r.stderr, file=sys.stderr)
        return r.returncode

    r = git("status", "--short")
    print(r.stdout.strip())
    if not r.stdout.strip():
        print("(nothing to commit)")
        r = git("push", "origin", "HEAD")
        print(r.stdout or "", end="")
        if r.stderr:
            print(r.stderr, file=sys.stderr)
        return r.returncode

    r = git(
        "commit",
        "-m",
        "Update wedding site: layout image and content",
    )
    print(r.stdout or "(committed)")
    if r.stderr:
        print(r.stderr, file=sys.stderr)
    if r.returncode != 0:
        return r.returncode

    r = git("push", "origin", "HEAD")
    print(r.stdout or "", end="")
    if r.stderr:
        print(r.stderr, file=sys.stderr)
    return r.returncode


if __name__ == "__main__":
    sys.exit(main() or 0)
