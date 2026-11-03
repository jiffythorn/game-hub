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


CSS_LINK = re.compile(r'<link rel="stylesheet" href="\.\./([^"]+\.css)"\s*/?>')
JS_LINK = re.compile(r'<script src="\.\./([^"]+\.js)"></script>')


def inline_css(html: str, css: dict[str, str]) -> str:
    if not CSS_LINK.search(html):
        raise RuntimeError("no ../*.css links found")

    def replace(match: re.Match[str]) -> str:
        name = match.group(1)
        if name not in css:
            raise RuntimeError(f"stylesheet {name} was not loaded")
        return f"<style>\n{css[name]}\n</style>"

    return CSS_LINK.sub(replace, html)


def inline_js(html: str, js: dict[str, str]) -> str:
    def replace(match: re.Match[str]) -> str:
        name = match.group(1)
        if name not in js:
            raise RuntimeError(f"javascript {name} was not loaded")
        return f"<script>\n{js[name]}\n</script>"
    return JS_LINK.sub(replace, html)


def make_standalone(html: str, name: str) -> str:
    html = html.replace('href="../index.html#games"', 'href="#"')
    html = html.replace('href="../index.html#download"', 'href="#"')
    html = html.replace('href="../index.html"', 'href="#"')
    html = re.sub(
        rf'<a class="btn btn-green btn-sm" href="\.\./downloads/{name}\.zip" download>⬇ Download</a>',
        "",
        html,
    )
    html = re.sub(
        r'\s*<a class="bingo-switch" href="[^"]+">.*?</a>',
        "",
        html,
        flags=re.S,
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
    css = {"style.css": (ROOT / "style.css").read_text(encoding="utf-8")}
    js: dict[str, str] = {}
    for page in sorted((ROOT / "games").glob("*.html")):
        name = page.stem
        html = page.read_text(encoding="utf-8")
        for sheet in CSS_LINK.findall(html):
            path = ROOT / sheet
            if not path.is_file():
                raise RuntimeError(f"{page.name} links missing stylesheet {sheet}")
            css.setdefault(sheet, path.read_text(encoding="utf-8"))
        for script in JS_LINK.findall(html):
            path = ROOT / script
            if not path.is_file():
                raise RuntimeError(f"{page.name} links missing javascript {script}")
            js.setdefault(script, path.read_text(encoding="utf-8"))
        html = make_standalone(inline_css(html, css), name)
        html = inline_js(html, js)
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
