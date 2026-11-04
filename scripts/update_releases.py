#!/usr/bin/env python3
"""Refresh a direct-download manifest from maintainers' official releases."""
from __future__ import annotations
import json
import os
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = {
    "zapret": "Flowseal/zapret-discord-youtube",
    "byebye": "romanvht/ByeByeDPI",
    "tgproxy": "Flowseal/tg-ws-proxy",
    "tgproxyandroid": "kamenwwcpp/tg-ws-proxy-android",
}
WARP_DOWNLOADS = [
    {"name": "Cloudflare WARP · Windows · MSI", "label": "Windows · MSI", "os": "Windows",
     "url": "https://downloads.cloudflareclient.com/v1/download/windows/ga"},
    {"name": "Cloudflare WARP · macOS · PKG", "label": "macOS · PKG", "os": "macOS",
     "url": "https://downloads.cloudflareclient.com/v1/download/macos/ga"},
    {"name": "Cloudflare WARP · Linux package repository", "label": "Linux · DEB / RPM repository",
     "os": "Linux", "url": "https://pkg.cloudflareclient.com/"},
    {"name": "1.1.1.1 + WARP · Google Play", "label": "Android · Google Play", "os": "Android",
     "url": "https://play.google.com/store/apps/details?id=com.cloudflare.onedotonedotonedotone"},
    {"name": "1.1.1.1 · App Store", "label": "iOS · App Store", "os": "iOS",
     "url": "https://apps.apple.com/app/1-1-1-1-faster-internet/id1423538627"},
]

def get_json(url: str):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "LEDERG-SQUAD-release-monitor"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=25) as response:
        return json.load(response)

def asset_details(project_id: str, asset: dict) -> dict:
    name = asset.get("name", "")
    low = name.lower()
    if project_id in {"byebye", "tgproxyandroid"}:
        platform = "Android"
    elif project_id == "zapret":
        platform = "Windows"
    elif "linux" in low:
        platform = "Linux"
    elif "macos" in low or "darwin" in low:
        platform = "macOS"
    else:
        platform = "Windows"

    arch = ""
    for pattern, label in [
        (r"arm64|aarch64", "ARM64"), (r"arm32|armeabi|32bit|x86(?=[._-]|$)", "32-bit / x86"),
        (r"x86_64|amd64|64bit", "x64"),
        (r"universal", "Universal"),
    ]:
        if re.search(pattern, low):
            arch = label
            break
    if "windows_7_32bit" in low:
        arch = "Windows 7 · 32-bit"
    elif "windows_7_64bit" in low:
        arch = "Windows 7 · 64-bit"

    if low.endswith(".tar.gz"):
        kind = "TAR.GZ"
    else:
        suffix = Path(low).suffix
        kind = suffix.lstrip(".").upper() if suffix else "BINARY"
    label = " · ".join(part for part in (platform, arch, kind) if part)
    key = ""
    if project_id == "zapret" and low.endswith(".zip"):
        key = "zip"
    elif project_id == "tgproxy" and "windows.exe" in low and "windows_7" not in low:
        key = "win64"
    elif "universal" in low:
        key = "universal"
    return {
        "name": name, "label": label or name, "os": platform, "key": key,
        "url": asset.get("browser_download_url", ""), "size": asset.get("size", 0),
    }

def main():
    path = ROOT / "releases.json"
    previous = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"projects": {}}
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "projects": previous.get("projects", {}),
        "warp": {"version": "latest", "download": WARP_DOWNLOADS[0]["url"],
                 "downloads": WARP_DOWNLOADS},
    }
    failures = []
    for key, repo in PROJECTS.items():
        try:
            release = get_json(f"https://api.github.com/repos/{repo}/releases/latest")
            # Keep every attached release asset, not just known extensions/architectures.
            assets = [asset_details(key, asset) for asset in release.get("assets", [])
                      if asset.get("browser_download_url")]
            if not assets:
                raise RuntimeError("latest release has no downloadable attached assets")
            assets.sort(key=lambda a: (a["key"] not in {"zip", "win64", "universal"}, a["name"].lower()))
            manifest["projects"][key] = {
                "repo": repo, "version": release.get("tag_name", "latest"),
                "published": (release.get("published_at") or "")[:10],
                "release_id": release.get("id"), "assets": assets,
            }
            print(f"{key}: {manifest['projects'][key]['version']} ({len(assets)} release assets)")
        except Exception as error:
            failures.append(f"{key}: {error}")
            print(f"WARNING: {key}: keeping last known release ({error})")
    if set(manifest["projects"]) != set(PROJECTS):
        raise SystemExit("One or more projects have no last-known release manifest; refusing an incomplete manifest")
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if failures:
        print("Some release APIs were unavailable; retained their previous manifest entries.")
    print(f"Updated {path}")

if __name__ == "__main__":
    main()
