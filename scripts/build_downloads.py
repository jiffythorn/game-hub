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
SITE_URL = "https://jiffythorn.github.io/game-hub"
# tools/ holds local-only operator pages (the credit minter), so it never
# ships in a download.
EXCLUDE_DIRS = {".git", ".github", "__pycache__", "tools"}
EXCLUDE_FILES = {".DS_Store"}


CSS_LINK = re.compile(r'<link rel="stylesheet" href="\.\./([^"]+\.css)"\s*/?>')


def inline_css(html: str, css: dict[str, str]) -> str:
    if not CSS_LINK.search(html):
        raise RuntimeError("no ../*.css links found")

    def replace(match: re.Match[str]) -> str:
        name = match.group(1)
        if name not in css:
            raise RuntimeError(f"stylesheet {name} was not loaded")
        return f"<style>\n{css[name]}\n</style>"

    return CSS_LINK.sub(replace, html)


def make_standalone(html: str, name: str) -> str:
    html = html.replace('href="../index.html#games"', 'href="#"')
    html = html.replace('href="../index.html#download"', 'href="#"')
    html = html.replace('href="../index.html"', 'href="#"')
    # The standalone copy has no sibling pages; point the terms and guestbook
    # links at the published site instead of leaving them to 404.
    html = html.replace('href="../terms.html', f'href="{SITE_URL}/terms.html')
    html = html.replace('href="../chat.html"', f'href="{SITE_URL}/chat.html"')
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
        if rel.parts[0] == "downloads" and p.name == SITE_ZIP:
            continue
        source: Path | str = p
        if p.suffix == ".html":
            html = p.read_text(encoding="utf-8")
            # The bundle cannot contain a copy of itself, so its self-download
            # button goes to the published bundle instead of a dead local path.
            html = html.replace(
                'href="downloads/game-hub-offline.zip"',
                f'href="{SITE_URL}/downloads/game-hub-offline.zip"',
            )
            source = html
        entries.append((f"game-hub/{rel.as_posix()}", source))
    entries.sort(key=lambda e: e[0])
    write_zip(OUT / SITE_ZIP, entries)


def build_game_zips() -> None:
    css = {"style.css": (ROOT / "style.css").read_text(encoding="utf-8")}
    for page in sorted((ROOT / "games").glob("*.html")):
        name = page.stem
        html = page.read_text(encoding="utf-8")
        for sheet in CSS_LINK.findall(html):
            path = ROOT / sheet
            if not path.is_file():
                raise RuntimeError(f"{page.name} links missing stylesheet {sheet}")
            css.setdefault(sheet, path.read_text(encoding="utf-8"))
        html = make_standalone(inline_css(html, css), name)
        write_zip(OUT / f"{name}.zip", [("index.html", html)])


def main() -> None:
    print("Building downloads…")
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    build_game_zips()
    build_site_zip()
    print("Done.")


if __name__ == "__main__":
    main()
