#!/usr/bin/env python3
"""Refresh official release downloads and upstream project documentation."""
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
DOC_SOURCES = {
    "zapret": [
        ("README · установка, стратегии и диагностика",
         "https://raw.githubusercontent.com/Flowseal/zapret-discord-youtube/main/README.md"),
    ],
    "byebye": [
        ("README · ByeByeDPI Android",
         "https://raw.githubusercontent.com/romanvht/ByeByeDPI/master/README.md"),
    ],
    "tgproxy": [
        ("README · обзор и быстрый старт",
         "https://raw.githubusercontent.com/Flowseal/tg-ws-proxy/main/docs/README.md"),
        ("Windows · установка и настройка Telegram Desktop",
         "https://raw.githubusercontent.com/Flowseal/tg-ws-proxy/main/docs/RU/README.windows.md"),
        ("Linux · установка и настройка Telegram Desktop",
         "https://raw.githubusercontent.com/Flowseal/tg-ws-proxy/main/docs/RU/README.linux.md"),
        ("macOS · установка и настройка Telegram Desktop",
         "https://raw.githubusercontent.com/Flowseal/tg-ws-proxy/main/docs/RU/README.macos.md"),
    ],
    "tgproxyandroid": [
        ("README · Telegram WS Proxy Android",
         "https://raw.githubusercontent.com/kamenwwcpp/tg-ws-proxy-android/main/README.md"),
    ],
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


def request_bytes(url: str) -> bytes:
    headers = {"User-Agent": "LEDERG-SQUAD-release-monitor/1.0"}
    token = os.environ.get("GITHUB_TOKEN")
    if token and "api.github.com" in url:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=35) as response:
        return response.read()


def get_json(url: str):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "LEDERG-SQUAD-release-monitor/1.0"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=35) as response:
        return json.load(response)


def fetch_readme(url: str) -> str:
    """Fetch upstream Markdown as text; never execute or interpret it in the workflow."""
    content = request_bytes(url).decode("utf-8-sig")
    if not content.strip():
        raise RuntimeError("README is empty")
    return content[:180_000]


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
        (r"windows_7_32bit", "Windows 7 · 32-bit"),
        (r"windows_7_64bit", "Windows 7 · 64-bit"),
        (r"x86_64|amd64|64bit", "x64"),
        (r"arm64|aarch64", "ARM64"),
        (r"arm32|armeabi|32bit|x86(?=[._-]|$)", "32-bit / x86"),
        (r"universal", "Universal"),
    ]:
        if re.search(pattern, low):
            arch = label
            break

    if low.endswith(".tar.gz"):
        kind = "TAR.GZ"
    else:
        suffix = Path(low).suffix
        kind = suffix.lstrip(".").upper() if suffix else "BINARY"
    label = " · ".join(part for part in (platform, arch, kind) if part)

    # Default selection is platform-specific. A macOS universal DMG is never the Windows build.
    key = ""
    if project_id == "zapret" and low.endswith(".zip"):
        key = "zip"
    elif project_id == "tgproxy" and low == "tgwsproxy_windows.exe":
        key = "win64"
    elif project_id in {"byebye", "tgproxyandroid"} and low.endswith(".apk") and "universal" in low:
        key = "universal"
    return {
        "name": name, "label": label or name, "os": platform, "key": key,
        "url": asset.get("browser_download_url", ""), "size": asset.get("size", 0),
    }


def asset_priority(project_id: str, asset: dict) -> tuple[int, str]:
    name = asset["name"].lower()
    if project_id == "tgproxy":
        order = {
            "tgwsproxy_windows.exe": 0,
            "tgwsproxy_windows_7_64bit.exe": 1,
            "tgwsproxy_windows_7_32bit.exe": 2,
            "tgwsproxy_windows_arm64.exe": 3,
            "tgwsproxy_macos_universal.dmg": 4,
            "tgwsproxy_linux_amd64.deb": 5,
            "tgwsproxy_linux_amd64.rpm": 6,
            "tgwsproxy_linux_amd64": 7,
        }
        return (order.get(name, 20), name)
    if project_id == "zapret":
        order = {".zip": 0, ".rar": 1, ".tar.gz": 2}
        return (next((p for ext, p in order.items() if name.endswith(ext)), 20), name)
    if project_id in {"byebye", "tgproxyandroid"}:
        if "universal" in name:
            return (0, name)
        if "arm64" in name:
            return (1, name)
        if "arm32" in name or "armeabi" in name:
            return (2, name)
        return (10, name)
    return (20, name)


def main():
    release_path = ROOT / "releases.json"
    docs_path = ROOT / "docs.json"
    old_release = json.loads(release_path.read_text(encoding="utf-8")) if release_path.exists() else {"projects": {}}
    old_docs = json.loads(docs_path.read_text(encoding="utf-8")) if docs_path.exists() else {"projects": {}}

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "projects": old_release.get("projects", {}),
        "warp": {"version": "latest", "download": WARP_DOWNLOADS[0]["url"],
                 "downloads": WARP_DOWNLOADS},
    }
    docs = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "projects": old_docs.get("projects", {}),
    }

    failures = []
    for key, repo in PROJECTS.items():
        try:
            release = get_json(f"https://api.github.com/repos/{repo}/releases/latest")
            # Preserve every attached release asset and its direct URL.
            assets = [asset_details(key, item) for item in release.get("assets", [])
                      if item.get("browser_download_url")]
            if not assets:
                raise RuntimeError("latest release has no downloadable attached assets")
            assets.sort(key=lambda item: asset_priority(key, item))
            manifest["projects"][key] = {
                "repo": repo, "version": release.get("tag_name", "latest"),
                "published": (release.get("published_at") or "")[:10],
                "release_id": release.get("id"), "assets": assets,
            }
            print(f"{key}: {manifest['projects'][key]['version']} ({len(assets)} assets)")
        except Exception as error:
            failures.append(f"release {key}: {error}")
            print(f"WARNING: release {key}: keeping last known release ({error})")

        sections = []
        old_sections = docs["projects"].get(key, {}).get("sections", [])
        for title, url in DOC_SOURCES[key]:
            try:
                text = fetch_readme(url)
                sections.append({"title": title, "url": url, "content": text})
                print(f"docs {key}: refreshed {title} ({len(text)} chars)")
            except Exception as error:
                failures.append(f"docs {key}/{title}: {error}")
                old = next((section for section in old_sections if section.get("url") == url), None)
                if old:
                    sections.append(old)
                    print(f"WARNING: docs {key}: retained last saved section {title}")
                else:
                    print(f"WARNING: docs {key}: unavailable section {title}")

        if sections:
            docs["projects"][key] = {
                "repo": repo,
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "sections": sections,
            }

    if set(manifest["projects"]) != set(PROJECTS):
        raise SystemExit("One or more projects have no last-known release manifest; refusing an incomplete manifest")
    if set(docs["projects"]) != set(PROJECTS):
        raise SystemExit("One or more projects have no cached documentation; refusing an incomplete docs manifest")

    release_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    docs_path.write_text(json.dumps(docs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if failures:
        print("Some upstream resources were unavailable; previous cached data was retained when possible.")
    print(f"Updated {release_path} and {docs_path}")


if __name__ == "__main__":
    main()
