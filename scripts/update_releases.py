#!/usr/bin/env python3
"""Refresh the public download manifest from official release APIs."""
from __future__ import annotations
import json
import os
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = {
    "zapret": ("Flowseal/zapret-discord-youtube", [
        (r"\.zip$", "Windows · ZIP", "Windows", "zip"),
        (r"\.rar$", "Windows · RAR", "Windows", "rar"),
    ]),
    "byebye": ("romanvht/ByeByeDPI", [
        (r"arm64-v8a.*\.apk$", "Android · ARM64", "Android", "arm64"),
        (r"armeabi-v7a.*\.apk$", "Android · ARM32", "Android", "arm32"),
        (r"universal.*\.apk$", "Android · Universal", "Android", "universal"),
        (r"x86-release.*\.apk$", "Android · x86", "Android", "x86"),
        (r"x86_64-release.*\.apk$", "Android · x86_64", "Android", "x64"),
    ]),
    "tgproxy": ("Flowseal/tg-ws-proxy", [
        (r"^TgWsProxy_windows\.exe$", "Windows · x64", "Windows", "win64"),
        (r"windows_7_32bit", "Windows 7 · 32-bit", "Windows", "win7x86"),
        (r"windows_7_64bit", "Windows 7 · 64-bit", "Windows", "win7x64"),
        (r"windows_arm64", "Windows · ARM64", "Windows", "winarm64"),
        (r"linux_amd64\.deb$", "Linux · DEB", "Linux", "deb"),
        (r"linux_amd64\.rpm$", "Linux · RPM", "Linux", "rpm"),
        (r"linux_amd64$", "Linux · Binary", "Linux", "linuxbin"),
        (r"macos_universal\.dmg$", "macOS · Universal", "macOS", "macos"),
    ]),
    "tgproxyandroid": ("kamenwwcpp/tg-ws-proxy-android", [
        (r"arm64\.apk$", "Android · ARM64", "Android", "arm64"),
        (r"universal\.apk$", "Android · Universal", "Android", "universal"),
        (r"arm32\.apk$", "Android · ARM32", "Android", "arm32"),
    ]),
}

def get_json(url: str):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "LEDERG-SQUAD-release-monitor"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=25) as response:
        return json.load(response)

def main():
    previous_path = ROOT / "releases.json"
    previous = json.loads(previous_path.read_text(encoding="utf-8")) if previous_path.exists() else {"projects": {}}
    manifest = {"generated_at": datetime.now(timezone.utc).isoformat(), "projects": previous.get("projects", {}), "warp": {
        "version": "latest", "download": "https://1111-releases.cloudflareclient.com/win/latest",
        "label": "Cloudflare WARP · Windows · MSI"
    }}
    failures = []
    for key, (repo, patterns) in PROJECTS.items():
        try:
            release = get_json(f"https://api.github.com/repos/{repo}/releases/latest")
            assets = []
            for pattern, label, os_name, asset_key in patterns:
                match = next((a for a in release.get("assets", []) if re.search(pattern, a.get("name", ""), re.I)), None)
                if match:
                    assets.append({"name": match["name"], "label": label, "os": os_name,
                                   "key": asset_key, "url": match["browser_download_url"],
                                   "size": match.get("size", 0)})
            if not assets:
                raise RuntimeError("latest release returned no recognized installer assets")
            manifest["projects"][key] = {
                "repo": repo, "version": release.get("tag_name", "latest"),
                "published": (release.get("published_at") or "")[:10],
                "release_id": release.get("id"), "assets": assets
            }
            print(f"{key}: {manifest['projects'][key]['version']} ({len(assets)} files)")
        except Exception as error:
            failures.append(f"{key}: {error}")
            print(f"WARNING: {key}: keeping last known release ({error})")
    if not manifest["projects"]:
        raise SystemExit("No release data available; refusing to write an empty manifest")
    previous_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if failures:
        print("Some release APIs were unavailable; retained their previous manifest entries.")
    print(f"Updated {previous_path}")

if __name__ == "__main__":
    main()
