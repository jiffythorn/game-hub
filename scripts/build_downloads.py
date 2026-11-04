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
EXCLUDE_DIRS = {".git", "downloads", ".github", "__pycache__", "artifacts", "scripts"}
EXCLUDE_FILES = {".DS_Store", ".gitignore", "PLAN.md"}


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
        r'\s*<a class="link hide-sm" href="\.\./chat\.html">.*?</a>',
        "",
        html,
    )
    html = re.sub(
        r'\s*<a class="link hide-sm" href="#">Download</a>',
        "",
        html,
    )
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


def make_offline_site(html: str) -> str:
    html = re.sub(
        r'\s*<a class="link hide-sm" href="#download">.*?</a>',
        "",
        html,
    )
    html = re.sub(
        r'\s*<a class="btn btn-green" href="downloads/game-hub-offline\.zip"[^>]*>.*?</a>',
        "",
        html,
        flags=re.S,
    )
    html = re.sub(
        r'\s*<a class="btn btn-ghost btn-sm" href="downloads/[^"]+\.zip"[^>]*>.*?</a>',
        "",
        html,
        flags=re.S,
    )
    html = html.replace(
        "Hit play and you're gaming in under a second — or download the whole pack and play with zero internet, forever.",
        "Hit play and you're gaming in under a second — this copy is ready with zero internet.",
    )
    html = html.replace(
        "<h3>⬇ Grab the whole arcade</h3>",
        "<h3>✓ This copy is already offline</h3>",
    )
    html = html.replace(
        "Download the complete site as a ZIP, unzip it, and double-click <code>index.html</code>. Every game works with no internet connection — ideal for planes, offline machines, or just keeping forever.",
        "This copy is already on your machine. Double-click <code>index.html</code> whenever you want to play — no internet connection required.",
    )
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
        if any(part in EXCLUDE_DIRS for part in rel.parts) or p.name in EXCLUDE_FILES:
            continue
        source: Path | str = p
        if rel.as_posix() == "index.html":
            source = make_offline_site(p.read_text(encoding="utf-8"))
        entries.append((f"game-hub/{rel.as_posix()}", source))
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
