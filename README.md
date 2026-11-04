# LEDERG SQUAD — Official Network Downloads

LEDERG SQUAD is a Russian-language download hub for official DPI utilities, Telegram proxy clients, and Cloudflare WARP. Each project has an internal information page with a description, installation notes, and direct download buttons.

**No repacks, third-party mirrors, or external project-page buttons.** Installer buttons link directly to files published by the original maintainers. LEDERG SQUAD does not host or modify third-party binaries.

## Catalog

- Flowseal/zapret-discord-youtube — Windows DPI utility
- romanvht/ByeByeDPI — Android DPI utility
- Flowseal/tg-ws-proxy — Telegram proxy for Windows, Linux, and macOS
- kamenwwcpp/tg-ws-proxy-android — Telegram proxy for Android
- Cloudflare WARP — Windows MSI installer, direct Cloudflare evergreen download

## Release monitoring

- `scripts/update_releases.py` reads each project's GitHub `releases/latest` API endpoint and writes direct asset URLs to `releases.json`.
- `.github/workflows/release-monitor.yml` runs every two hours and can also be started manually.
- The workflow preserves the last known manifest entry if an upstream API is temporarily unavailable.
- The website reads the committed manifest first and can also refresh GitHub release metadata in the visitor's browser.
- WARP uses Cloudflare's evergreen Windows download endpoint: `https://1111-releases.cloudflareclient.com/win/latest`.

## Safety

- The website does not claim that a binary has been independently audited or is malware-free.
- Check publisher signatures, checksums when provided, and scan downloads before running them.
- Some utilities modify network behavior or require elevated privileges. Read the internal installation notes before use.
- ByeByeDPI is not a remote VPN and does not encrypt all device traffic or hide the user's IP address.

## GitHub Pages

The `pages.yml` workflow runs smoke tests and JavaScript syntax validation, then deploys the static site to GitHub Pages.
