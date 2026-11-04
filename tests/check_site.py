from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "index.html").read_text(encoding="utf-8")
MANIFEST = ROOT / "releases.json"
MONITOR = (ROOT / "scripts" / "update_releases.py").read_text(encoding="utf-8")
WORKFLOW = (ROOT / ".github" / "workflows" / "release-monitor.yml").read_text(encoding="utf-8")


class LedgergSquadSmokeTests(unittest.TestCase):
    def test_main_app_mount_and_navigation_exist(self):
        self.assertIn('id="app"', HTML)
        self.assertIn('id="navLinks"', HTML)
        self.assertIn("window.addEventListener('hashchange',render)", HTML)

    def test_catalog_contains_only_the_four_network_tools(self):
        for project_id in ("zapret", "byebye", "tgproxy", "tgproxyandroid"):
            self.assertRegex(HTML, rf"id:'{project_id}'")
        for old_project in ("music", "python", "neiro", "drive", "messenger"):
            self.assertNotRegex(HTML, rf"id:'{old_project}'")

    def test_each_card_uses_official_github_source_and_release_api(self):
        for repo in (
            "Flowseal/zapret-discord-youtube",
            "romanvht/ByeByeDPI",
            "Flowseal/tg-ws-proxy",
            "kamenwwcpp/tg-ws-proxy-android",
        ):
            self.assertIn(repo, HTML)
        self.assertIn("api.github.com/repos/", HTML)
        self.assertIn("/releases/latest", HTML)

    def test_original_previews_and_direct_downloads_are_present(self):
        self.assertIn("preview-dark.png", HTML)
        self.assertIn("user-attachments/assets/7c9b9f2a-fc60-4aee-b93d-db950e24555c", HTML)
        self.assertIn("browser_download_url", HTML)
        self.assertIn("download_url", HTML)

    def test_android_architecture_choices_are_documented(self):
        for variant in ("arm64", "universal", "arm32"):
            self.assertIn(variant, HTML)

    def test_warp_has_preview_and_direct_official_installer(self):
        self.assertIn("https://downloads.cloudflareclient.com/v1/download/windows/ga", HTML)
        self.assertIn("warp-preview", HTML)
        self.assertIn("warp-visual", HTML)
        self.assertIn("Cloudflare WARP", HTML)

    def test_details_are_internal_and_no_external_source_navigation(self):
        self.assertIn("Как работает", HTML)
        self.assertIn("Документация", HTML)
        self.assertNotIn("ОТКРЫТЬ ВСЕ РЕЛИЗЫ", HTML)
        self.assertNotIn("GitHub repository", HTML)
        self.assertNotIn("Cloudflare Docs", HTML)

    def test_release_monitor_and_direct_download_links(self):
        self.assertIn("releases.json", HTML)
        self.assertIn("browser_download_url", HTML)
        self.assertIn("download_url", HTML)

    def test_footer_has_native_telegram_contact_and_discord(self):
        self.assertIn("tg://resolve?domain=LEDERG_ru", HTML)
        self.assertIn("@LEDERG_ru", HTML)
        self.assertIn("https://discord.gg/kDRMWqKmZp", HTML)

    def test_anti_fake_and_source_disclosure_are_present(self):
        self.assertIn("ТОЛЬКО ОФИЦИАЛЬНЫЕ ИСТОЧНИКИ", HTML)
        self.assertIn("не перепаковывает", HTML)

    def test_release_monitor_manifest_and_schedule_exist(self):
        self.assertTrue(MANIFEST.exists())
        self.assertIn("api.github.com/repos/", MONITOR)
        self.assertIn("schedule:", WORKFLOW)
        self.assertIn("cron:", WORKFLOW)
        self.assertIn("releases.json", HTML)


    def test_preview_click_opens_internal_tool_page(self):
        self.assertIn('class="card-preview preview-open"', HTML)
        self.assertIn('href="#/tool/', HTML)

    def test_all_release_assets_are_listed_not_only_hardcoded_archives(self):
        self.assertIn('for asset in release.get("assets", [])', MONITOR)
        self.assertIn('browser_download_url', MONITOR)
        self.assertIn('release.assets.map(a=>normaliseAsset', HTML)

    def test_warp_offers_all_consumer_platform_download_routes(self):
        for platform in ("Windows", "macOS", "Linux", "Android", "iOS"):
            self.assertIn(platform, HTML)
        self.assertIn("downloads.cloudflareclient.com/v1/download/windows/ga", HTML)
        self.assertIn("downloads.cloudflareclient.com/v1/download/macos/ga", HTML)
        self.assertIn("pkg.cloudflareclient.com", HTML)
        self.assertIn("play.google.com/store/apps/details?id=com.cloudflare.onedotonedotonedotone", HTML)
        self.assertIn("apps.apple.com/app/1-1-1-1-faster-internet/id1423538627", HTML)

    def test_site_purpose_explains_verified_originals_and_stealer_risk(self):
        self.assertIn("во избежание стиллеров", HTML)
        self.assertIn("проверенных источников", HTML)
        self.assertIn("независимым аудитом", HTML)

    def test_external_links_open_safely(self):
        for anchor in re.findall(r'<a[^>]+target="_blank"[^>]*>', HTML):
            self.assertIn('rel="noopener noreferrer"', anchor)


if __name__ == "__main__":
    unittest.main(verbosity=2)
