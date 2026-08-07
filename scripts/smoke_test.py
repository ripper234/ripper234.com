#!/usr/bin/env python3
"""Local integrity and basic accessibility checks for the static site."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys

ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = [ROOT / "index.html", ROOT / "work-with-me" / "index.html", ROOT / "404.html"]


class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.refs: list[tuple[str, str]] = []
        self.ids: list[str] = []
        self.images_without_alt: list[str] = []
        self.unsafe_blank_links: list[str] = []
        self.h1_count = 0
        self.title_count = 0
        self._inside_title = False
        self._title_has_text = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"] or "")
        if tag in {"a", "link"} and values.get("href"):
            href = values["href"] or ""
            self.refs.append((tag, href))
            if tag == "a" and values.get("target") == "_blank":
                rel = set((values.get("rel") or "").split())
                if "noopener" not in rel:
                    self.unsafe_blank_links.append(href)
        if tag in {"img", "script"} and values.get("src"):
            self.refs.append((tag, values["src"] or ""))
        if tag == "img" and "alt" not in values:
            self.images_without_alt.append(values.get("src") or "(missing src)")
        if tag == "h1":
            self.h1_count += 1
        if tag == "title":
            self._inside_title = True
            self._title_has_text = False

    def handle_data(self, data: str) -> None:
        if self._inside_title and data.strip():
            self._title_has_text = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            if self._title_has_text:
                self.title_count += 1
            self._inside_title = False


def local_target(source: Path, ref: str) -> Path | None:
    parsed = urlsplit(ref)
    if parsed.scheme or parsed.netloc or ref.startswith(("#", "mailto:", "tel:")):
        return None
    path = unquote(parsed.path)
    if not path:
        return None
    target = (ROOT / path.lstrip("/")) if path.startswith("/") else (source.parent / path)
    if target.is_dir():
        target = target / "index.html"
    return target.resolve()


def fragment_target(source: Path, ref: str) -> tuple[Path, str] | None:
    parsed = urlsplit(ref)
    if parsed.scheme or parsed.netloc or not parsed.fragment:
        return None
    if parsed.path:
        target = local_target(source, ref)
        if target is None:
            return None
    else:
        target = source.resolve()
    return target, unquote(parsed.fragment)


def parse_file(path: Path) -> SiteParser:
    parser = SiteParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def main() -> int:
    errors: list[str] = []
    parsed_files: dict[Path, SiteParser] = {}

    for html_file in HTML_FILES:
        if not html_file.exists():
            errors.append(f"Missing HTML file: {html_file.relative_to(ROOT)}")
            continue
        parser = parse_file(html_file)
        parsed_files[html_file.resolve()] = parser
        label = html_file.relative_to(ROOT)

        duplicate_ids = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
        if duplicate_ids:
            errors.append(f"{label}: duplicate ids: {', '.join(duplicate_ids)}")
        if parser.images_without_alt:
            errors.append(f"{label}: image(s) missing alt attributes")
        if parser.unsafe_blank_links:
            errors.append(f"{label}: target=_blank link(s) missing rel=noopener")
        if parser.h1_count != 1:
            errors.append(f"{label}: expected one h1, found {parser.h1_count}")
        if parser.title_count != 1:
            errors.append(f"{label}: expected one non-empty title, found {parser.title_count}")

        for tag, ref in parser.refs:
            target = local_target(html_file, ref)
            if target is not None and not target.exists():
                errors.append(f"{label}: broken local {tag} reference {ref!r}")

    # Check that local fragment links point to actual element ids.
    for html_file, parser in parsed_files.items():
        for tag, ref in parser.refs:
            if tag != "a":
                continue
            fragment = fragment_target(html_file, ref)
            if fragment is None:
                continue
            target, element_id = fragment
            target_parser = parsed_files.get(target)
            if target_parser is None and target.exists() and target.suffix == ".html":
                target_parser = parse_file(target)
                parsed_files[target] = target_parser
            if target_parser is not None and element_id not in target_parser.ids:
                errors.append(
                    f"{html_file.relative_to(ROOT)}: fragment {ref!r} has no matching id"
                )

    required = [
        ROOT / "assets" / "css" / "styles.css",
        ROOT / "assets" / "js" / "main.js",
        ROOT / ".github" / "workflows" / "pages.yml",
        ROOT / "Tasks.md",
        ROOT / "README.md",
        ROOT / "robots.txt",
        ROOT / "sitemap.xml",
        ROOT / ".nojekyll",
    ]
    for path in required:
        if not path.exists():
            errors.append(f"Missing required file: {path.relative_to(ROOT)}")

    # A CNAME file would prematurely redirect the separate project preview.
    if (ROOT / "CNAME").exists():
        errors.append("Unexpected CNAME file: add the custom domain only after preview approval")

    if errors:
        print("Smoke test failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Smoke test passed: {len(HTML_FILES)} HTML files, local references, "
        "fragments, headings, image alt text, and safe external links checked."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
