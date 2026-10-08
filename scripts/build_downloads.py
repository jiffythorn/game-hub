#!/usr/bin/env python3
"""Build downloadable ZIPs into downloads/.

Produces:
  downloads/game-hub-offline.zip  - the whole site, runs from a folder
  downloads/<game>.zip            - one self-contained game file (index.html)

Run:  python3 scripts/build_downloads.py
"""

from __future__ import annotations

import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "downloads"

SITE_ZIP = "game-hub-offline.zip"
EXCLUDE_DIRS = {".git", "downloads", ".github", "__pycache__"}
EXCLUDE_FILES = {".DS_Store"}


def inline_css(html: str, css: str) -> str:
    pattern = re.compile(
        r'<link rel="stylesheet" href="\.\./style\.css"\s*/?>'
    )
    if not pattern.search(html):
        raise RuntimeError("style.css link not found")
    return pattern.sub(f"<style>\n{css}\n</style>", html, count=1)


def make_standalone(html: str, name: str) -> str:
    html = html.replace('href="../index.html#games"', 'href="#"')
    html = html.replace('href="../index.html#download"', 'href="#"')
    html = html.replace('href="../index.html"', 'href="#"')
    html = re.sub(
        rf'<a class="btn btn-green btn-sm" href="\.\./downloads/{name}\.zip" download>⬇ Download</a>',
        "",
        html,
    )
    html = html.replace("— Game Hub", "— Game Hub (offline copy)")
    return html


def write_zip(path: Path, entries: list[tuple[str, Path | str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for arcname, source in entries:
            if isinstance(source, str):
                z.writestr(arcname, source)
            else:
                z.write(source, arcname)
    print(f"  {path.relative_to(ROOT)}  ({path.stat().st_size:,} bytes)")


def build_site_zip() -> None:
    entries = []
    for p in sorted(ROOT.rglob("*")):
        if p.is_dir():
            continue
        rel = p.relative_to(ROOT)
        if rel.parts[0] in EXCLUDE_DIRS or p.name in EXCLUDE_FILES:
            continue
        entries.append((f"game-hub/{rel.as_posix()}", p))
    entries.sort(key=lambda e: e[0])
    write_zip(OUT / SITE_ZIP, entries)


def build_game_zips() -> None:
    css = (ROOT / "style.css").read_text(encoding="utf-8")
    for page in sorted((ROOT / "games").glob("*.html")):
        name = page.stem
        html = page.read_text(encoding="utf-8")
        html = make_standalone(inline_css(html, css), name)
        write_zip(OUT / f"{name}.zip", [("index.html", html)])


def main() -> None:
    print("Building downloads…")
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    build_site_zip()
    build_game_zips()
    print("Done.")


if __name__ == "__main__":
    main()
