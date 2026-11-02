#!/usr/bin/env python3
"""Check that relative links in the repository's Markdown files resolve.

External http(s) links are not fetched (they are flaky in CI); only links to
files, directories, and heading anchors inside this repository are checked.

Usage:  python tools/check_md_links.py [repo_root]
Exit code 0 if every relative link resolves, 1 otherwise.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
SKIP_DIRS = {".git", "node_modules", ".venv", "venv"}


def github_slug(text: str) -> str:
    """Approximate GitHub's heading-anchor algorithm."""
    text = re.sub(r"`([^`]*)`", r"\1", text)          # inline code
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)  # links
    text = text.strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)               # drop punctuation
    return text.replace(" ", "-")


def strip_code(lines: list[str]) -> list[str]:
    out, in_fence = [], False
    for line in lines:
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else re.sub(r"`[^`]*`", "", line))
    return out


def anchors_of(path: Path) -> set[str]:
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    for line in strip_code(path.read_text(encoding="utf-8").splitlines()):
        m = HEADING_RE.match(line)
        if not m:
            continue
        slug = github_slug(m.group(2))
        n = counts.get(slug, 0)
        anchors.add(slug if n == 0 else f"{slug}-{n}")
        counts[slug] = n + 1
    return anchors


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    md_files = [
        p for p in root.rglob("*.md")
        if not any(part in SKIP_DIRS for part in p.relative_to(root).parts)
    ]
    errors: list[str] = []
    checked = 0
    for md in sorted(md_files):
        lines = strip_code(md.read_text(encoding="utf-8").splitlines())
        for lineno, line in enumerate(lines, 1):
            for target in LINK_RE.findall(line):
                if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
                    continue  # http:, https:, mailto:, etc.
                checked += 1
                path_part, _, anchor = target.partition("#")
                dest = (md.parent / path_part).resolve() if path_part else md
                rel = md.relative_to(root)
                if not dest.exists():
                    errors.append(f"{rel}:{lineno}: missing target '{target}'")
                    continue
                if anchor and dest.is_file() and dest.suffix == ".md":
                    if anchor.lower() not in anchors_of(dest):
                        errors.append(f"{rel}:{lineno}: missing anchor '#{anchor}' in {dest.relative_to(root)}")
    for e in errors:
        print(e)
    print(f"checked {checked} relative links in {len(md_files)} Markdown files: "
          f"{'OK' if not errors else f'{len(errors)} broken'}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
