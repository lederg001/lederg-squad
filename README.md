# LEDERG SQUAD

Official static software hub for the LEDERG project family.

## Included

- Responsive black/red LEDERG interface.
- Project catalog with category filters and instant search.
- Dedicated project profile, README/instructions, and change-history views.
- Cloudflare WARP information page with official Cloudflare download links.
- Progressive Web App manifest and a small offline cache.
- GitHub Pages workflow.

## Preview locally

Open `index.html` directly, or serve the repository over HTTP:

```bash
python -m http.server 8080
```

Then open `http://localhost:8080`.

## Publish with GitHub Pages

1. Open **Settings → Pages** in this repository.
2. Choose **GitHub Actions** as the build and deployment source.
3. The workflow in `.github/workflows/pages.yml` publishes the static site on pushes to `main`.
4. Open the Pages URL shown by GitHub after the workflow succeeds.

## Custom domain

The previous `lederg-squad.cc.cd` domain is intentionally not configured in this repository. Attach it only when you are ready to move the custom domain from the previous Pages deployment. Do not change DNS records until the Pages custom-domain setting is ready.

## Notes

This is a static site. It does not need a backend, secrets, or a build step. Project links are external; current releases and downloadable binaries remain hosted by their respective project sources.
