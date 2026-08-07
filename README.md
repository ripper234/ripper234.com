# ripper234.com

Static recreation of the public Wix site at `ripper234.com`, prepared for GitHub Pages.

## What is included

- Home page with the current public sections and links.
- `/work-with-me/` page.
- Responsive, dependency-free HTML/CSS/JavaScript.
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

The current copy references five public images on Wix’s CDN. This preserves fidelity without blocking the first preview, but it is not a permanent Wix-independent archive. Download the originals from Wix Media Manager and move them into `assets/images/` before canceling Wix.
