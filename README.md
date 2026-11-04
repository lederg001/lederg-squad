# LEDERG SQUAD — Official Network Downloads

LEDERG SQUAD is a Russian-language download hub for DPI utilities, Telegram proxy clients, and Cloudflare WARP.

The site exists so people do not confuse original releases with fake repacks and stealer-laced copies. It collects direct installer links from the original project maintainers and official Cloudflare distribution channels, with internal descriptions and installation notes. This helps lower the risk of downloading malware from imitation pages.

**Source verification is not an independent malware audit.** LEDERG SQUAD does not host, modify, or repackage third-party binaries. Users should still verify signatures/checksums where available and scan files before running them.

## Catalog

- Flowseal/zapret-discord-youtube — Windows DPI utility; every attached asset in the latest release is listed.
- romanvht/ByeByeDPI — Android DPI utility; all APK architectures from latest releases are listed.
- Flowseal/tg-ws-proxy — Telegram proxy for Windows, Linux, and macOS; all release assets are listed.
- kamenwwcpp/tg-ws-proxy-android — Telegram proxy for Android; all APK variants are listed.
- Cloudflare WARP — consumer client install links for Windows, macOS, Linux, Android, and iOS.

The project previews on the homepage are clickable and open internal LEDERG SQUAD detail pages. Compact direct-download buttons are also displayed over each preview (for example, TG WS Proxy defaults specifically to `TgWsProxy_windows.exe`). Detail pages include program descriptions, installation information, release versions, and every attached direct-download asset.

Maintainer README files are refreshed into `docs.json` and rendered inside each internal detail page. TG WS Proxy includes its main README plus dedicated Windows, Linux, and macOS installation guides. Markdown is rendered with HTML stripped/escaped; the original documentation is presented as read-only content.

## WARP platform destinations

- Windows: official MSI endpoint, `https://downloads.cloudflareclient.com/v1/download/windows/ga`.
- macOS: official PKG endpoint, `https://downloads.cloudflareclient.com/v1/download/macos/ga`.
- Linux: Cloudflare's official DEB/RPM package repository, `https://pkg.cloudflareclient.com/`.
- Android: official Google Play listing for 1.1.1.1 + WARP.
- iOS: official App Store listing for 1.1.1.1.

Android and iOS use the official application stores. Linux uses a distribution-specific package repository rather than one universal installer.

## Release monitoring

- `scripts/update_releases.py` reads each project's GitHub `releases/latest` endpoint and writes **every attached release asset** and its direct download URL to `releases.json`.
- The same monitor refreshes the projects' upstream README files and platform-specific documentation into `docs.json`.
- `.github/workflows/release-monitor.yml` runs every two hours and can also be started manually.
- The workflow retains the last known release entry when an upstream API is temporarily unavailable.
- The website loads the committed manifest first and can refresh release data in the visitor's browser.
- When either the release manifest or README documentation changes, the workflow republishes the Pages website.

## Safety

- No random mirrors or repacked installers are linked.
- Check publisher signatures, checksums when provided, and scan downloads before running them.
- Some utilities change network behavior or require elevated privileges. Read their internal installation notes before use.
- ByeByeDPI is not a remote VPN and does not encrypt all device traffic or hide the user's IP address.

## GitHub Pages

The `pages.yml` workflow runs smoke tests and JavaScript syntax validation, then deploys the static site to GitHub Pages.
