# ripper234.com

Static, fidelity-first recreation of the public Wix site at `ripper234.com`, prepared for GitHub Pages.

## What is included

- Home page with the current public sections and links.
- `/work-with-me/` page.
- Responsive, framework-free HTML/CSS/JavaScript.
- Original Wix layout, typography, gradients, cards, icons, section order, and links.
- GitHub Pages deployment workflow.
- SEO basics: canonical metadata, sitemap, robots file, and 404 page.
- Migration and content-refresh plan in [`Tasks.md`](Tasks.md).

## Local preview

```bash
python3 -m http.server 8080
```

Then open `http://localhost:8080/`.

Run the local smoke test:

```bash
python3 scripts/smoke_test.py
```

## Deploy the separate preview

1. Push `main` to `ripper234/ripper234.com`.
2. Open **Settings → Pages**.
3. Select **GitHub Actions** as the source.
4. The preview should publish at `https://ripper234.github.io/ripper234.com/`.

Do not add the custom domain until the preview has been reviewed. The exact cutover checklist is in [`Tasks.md`](Tasks.md).

## Important asset note

Project, portfolio, and organization SVGs are stored locally. The remaining hero, decorative, photographic, and font files still load from Wix’s public CDNs. This preserves fidelity without blocking the preview, but it is not a permanent Wix-independent archive. Download those originals and self-host them before canceling Wix.
