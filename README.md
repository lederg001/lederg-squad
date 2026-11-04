# LEDERG SQUAD — Official Network Tools

LEDERG SQUAD is a Russian-language directory of official sources and downloads for DPI tools, Telegram connection utilities, and Cloudflare WARP.

**The site does not repackage or host third-party installers.** Program descriptions, releases, and direct download links point to the original project maintainers.

## Catalog

| Project | Official source | Platforms |
|---|---|---|
| zapret-discord-youtube | [Flowseal/zapret-discord-youtube](https://github.com/Flowseal/zapret-discord-youtube) | Windows |
| ByeByeDPI | [romanvht/ByeByeDPI](https://github.com/romanvht/ByeByeDPI) | Android |
| Telegram WS Proxy | [Flowseal/tg-ws-proxy](https://github.com/Flowseal/tg-ws-proxy) | Windows, Linux, macOS |
| Telegram WS Proxy Android | [kamenwwcpp/tg-ws-proxy-android](https://github.com/kamenwwcpp/tg-ws-proxy-android) | Android |
| Cloudflare WARP | [Cloudflare Windows documentation](https://developers.cloudflare.com/warp-client/get-started/windows/) | Windows |

The four GitHub projects expose their current `releases/latest` assets through the GitHub public API. A static fallback list is included, so the download cards remain usable if the API is rate-limited or temporarily unavailable.

## Safety model

- No third-party mirrors or re-packed installers are linked.
- Download links are built from assets exposed by the official GitHub Releases API.
- The site does not claim that a binary has been independently audited or is malware-free.
- Verify the repository owner, release tag, file name, checksum/signature when available, and scan downloads before running them.
- Read each project's own installation notes. Some tools require elevated privileges or change network behavior.

LEDERG SQUAD is an independent index and is not affiliated with the maintainers of the listed projects or with Cloudflare.

## Preview locally

Open `index.html`, or serve this directory over HTTP:

```bash
python -m http.server 8080
```

Then open `http://localhost:8080`.

## GitHub Pages

1. Open **Settings → Pages**.
2. Set **Source** to **GitHub Actions**.
3. The workflow in `.github/workflows/pages.yml` runs catalog checks and publishes the static site on pushes to `main`.
4. Open the Pages URL shown by GitHub after deployment succeeds.

## Technical notes

- Static HTML, CSS, and JavaScript; no backend or secrets required.
- Responsive black/red LEDERG interface.
- Cards use previews hosted by the projects' public GitHub repositories.
- Latest version and release assets refresh from GitHub when a visitor opens the site.
- PWA manifest and a small offline cache are included.

