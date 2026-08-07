# ripper234.com migration tasks

Last updated: 2026-08-07

## Execution status (2026-08-07)

- [x] Scanned the public Wix home page and public Work With Me page.
- [x] Prepared and locally validated a static GitHub Pages copy.
- [x] Added a custom GitHub Actions Pages deployment workflow.
- [x] Prepared this migration, rollback, and future content-refresh checklist.
- [x] Published the prepared 13-file website snapshot to remote `main` in commit [`06511ff`](https://github.com/ripper234/ripper234.com/commit/06511ffe895e2fb4dd43d0b2dec3879513a73701), on top of the user-created root commit, without force-pushing. The remote tree exactly matches the locally validated tree at prepared commit `97eb6b5`.
- [ ] Enable Pages via GitHub Actions: [workflow run #1](https://github.com/ripper234/ripper234.com/actions/runs/31182510947) triggered successfully but failed at **Configure Pages** because the new repository does not yet have a Pages site. Select **GitHub Actions** once in **Repository → Settings → Pages**, then rerun the workflow.
- [ ] Change DNS: intentionally deferred until the separate preview is reviewed and requires access to the authoritative DNS provider.
- [ ] Replace Wix-hosted images with local files before Wix is canceled.

## Goal

Create a static, maintainable copy of the current Wix website in `ripper234/ripper234.com`, publish it first as a separate GitHub Pages preview, then move `ripper234.com` to GitHub Pages without changing the public domain. After the migration is stable, make **Balance** and **Build** the primary projects and move **Fredo.ai** and **Whatever Works** into an archive.

## 0. Current-site capture and static copy

- [x] Inventory the public Wix site.
  - [x] Home page and in-page sections: Home, Portfolio, Nonprofits, Verticals, Work With Me, Contact, Live Calls.
  - [x] Public page: `/work-with-me`.
  - [x] Preserve public text, outbound links, navigation, and the visual purple/black/white language.
- [x] Build a framework-free static copy suitable for GitHub Pages.
  - [x] Responsive home page.
  - [x] Responsive `/work-with-me/` page.
  - [x] Mobile navigation and accessibility basics.
  - [x] Metadata, canonical URLs, `robots.txt`, `sitemap.xml`, and a custom `404.html`.
- [x] Add a GitHub Actions Pages deployment workflow.
- [x] Add local smoke tests and preview instructions.
- [ ] **Before canceling Wix:** download and self-host the five referenced Wix media assets. The first copy deliberately uses the existing `static.wixstatic.com` URLs so the visual content is preserved, but this is not a fully independent archive.

## 1. Publish the separate GitHub Pages preview

Target preview URL: `https://ripper234.github.io/ripper234.com/`

- [x] Publish the prepared website snapshot to `https://github.com/ripper234/ripper234.com`.
  - Safely reconciled the user-created root commit `653dc37` with the prepared site by creating child commit [`06511ff`](https://github.com/ripper234/ripper234.com/commit/06511ffe895e2fb4dd43d0b2dec3879513a73701); no force-push was used.
  - Remote tree `b75e43e` exactly matches the local tree at prepared commit `97eb6b5`. The original commit SHA could not be retained because the manually created root is a different parent, but the complete website content and file modes were preserved.
- [ ] In GitHub: **Repository → Settings → Pages → Build and deployment → Source: GitHub Actions**.
- [ ] Open the latest **Deploy static site to GitHub Pages** workflow run and confirm it succeeds.
  - Initial run: [#1](https://github.com/ripper234/ripper234.com/actions/runs/31182510947) failed at **Configure Pages** with `Get Pages site failed: Not Found`; checkout and workflow triggering both succeeded.
- [ ] Test the preview on desktop and mobile:
  - [ ] Home sections and anchor navigation.
  - [ ] `/work-with-me/`.
  - [ ] External links.
  - [ ] Keyboard navigation.
  - [ ] Images load from Wix CDN.
  - [ ] No console errors.
- [ ] Keep this preview URL live until the custom-domain cutover is verified.

## 2. Prepare a safe domain cutover

Do not change the domain registrar or nameservers. Change only the web-serving DNS records. Preserve email, verification, and every unrelated subdomain.

- [ ] At the domain’s current authoritative DNS provider, export or screenshot every current DNS record. If DNS is managed in Wix, use **Domains → Domain Actions → Manage DNS records**.
- [ ] Record the current values for:
  - [ ] Apex/root A records.
  - [ ] `www` CNAME.
  - [ ] MX records and mail-related TXT/CNAME records.
  - [ ] `_github-pages-challenge-ripper234` if already present.
  - [ ] Existing subdomains, especially `workwithme`, `v1`, and `jarvis`.
- [ ] Lower TTL for the root A and `www` CNAME records to the lowest practical value before cutover, ideally at least one current TTL period in advance.
- [ ] In GitHub account **Settings → Pages**, add and verify `ripper234.com`; add the TXT record GitHub gives you and keep it permanently.
- [ ] In repository **Settings → Pages**, set the custom domain to `www.ripper234.com` **before** pointing DNS to GitHub.
- [ ] Confirm the GitHub preview is complete and obtain a rollback screenshot of the old Wix A/CNAME values.

## 3. Move the existing domain from Wix hosting to GitHub Pages

GitHub Pages web DNS values:

- Apex/root A records (in Wix, leave the host blank when documentation says `@`):
  - `185.199.108.153`
  - `185.199.109.153`
  - `185.199.110.153`
  - `185.199.111.153`
- `www` CNAME: `ripper234.github.io`

Cutover:

- [ ] Replace only the Wix root website A record(s) with the four GitHub Pages A records above.
- [ ] Replace only the Wix `www` website record with `CNAME → ripper234.github.io`.
- [ ] Do **not** delete or modify MX, mail TXT, verification, or unrelated subdomain records.
- [ ] Wait for GitHub’s DNS check and TLS certificate provisioning.
- [ ] Enable **Enforce HTTPS** in GitHub Pages when available.
- [ ] Verify all four URLs:
  - [ ] `http://ripper234.com`
  - [ ] `https://ripper234.com`
  - [ ] `http://www.ripper234.com`
  - [ ] `https://www.ripper234.com`
- [ ] Confirm one canonical host redirects cleanly and there is no redirect loop.
- [ ] Re-test `workwithme.ripper234.com`, `v1.ripper234.com`, `jarvis.ripper234.com`, and email delivery.
- [ ] Keep the Wix site and plan intact for at least 7 days after cutover.

Rollback if the cutover fails:

- [ ] Restore the recorded Wix root A and `www` CNAME values.
- [ ] Remove or pause the repository custom domain only after the old Wix records are restored.
- [ ] Re-test HTTPS, email, and subdomains.

## 4. Make the site independent from Wix

- [ ] Download the original hero, decorative, skyline, and meeting images from Wix Media Manager.
- [ ] Store optimized local copies under `assets/images/`.
- [ ] Replace all `static.wixstatic.com` references with local relative paths.
- [ ] Re-run visual and performance checks.
- [ ] Only then consider downgrading or canceling the Wix website plan. Domain registration/DNS can remain at Wix if desired.

## 5. Refresh primary projects after migration

- [ ] Add **Balance** as a primary project.
  - [ ] Confirm public URL.
  - [ ] Final one-line description.
  - [ ] Logo or hero image.
  - [ ] Primary call to action.
- [ ] Add **Build** as a primary project.
  - [ ] Confirm whether the public name is “Build”, “ron.build”, or another label.
  - [ ] Confirm public URL.
  - [ ] Final one-line description.
  - [ ] Logo or hero image.
- [ ] Move **Fredo.ai** and **Whatever Works** into an “Archived projects” section; preserve their links and a short historical note.
- [ ] Decide whether “And more / Kugelblitz” stays primary, moves to archive, or becomes a general projects index.
- [ ] Update page title, description, Open Graph text/image, structured data, and project ordering.
- [ ] Add a visible “current focus” date so visitors can distinguish active projects from historical work.

## 6. Post-migration improvements

- [ ] Correct copy errors only after the fidelity copy is approved (`Whatever Work`, `Communiction`, `Intersting`, etc.).
- [ ] Add links or context for portfolio company names where appropriate.
- [ ] Decide whether `workwithme.ripper234.com` should keep its Wix version, redirect to `/work-with-me/`, or become a GitHub Pages-hosted subdomain.
- [ ] Add privacy-friendly analytics only if useful.
- [ ] Add automated broken-link and Lighthouse checks in GitHub Actions.
- [ ] Archive a final full-page screenshot of the old Wix site for reference.

## Official references

- GitHub Pages publishing source: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- GitHub Pages custom domains and current A records: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site
- GitHub Pages domain verification: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages
- GitHub Pages HTTPS: https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https
- Wix DNS management: https://support.wix.com/en/article/managing-dns-records-in-your-wix-account
