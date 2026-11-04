from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "index.html").read_text(encoding="utf-8")


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

    def test_warp_links_to_the_official_windows_instructions(self):
        self.assertIn("developers.cloudflare.com/warp-client/get-started/windows/", HTML)
        self.assertIn("CLOUDFLARE WARP", HTML)

    def test_anti_fake_and_source_disclosure_are_present(self):
        self.assertIn("ТОЛЬКО ОФИЦИАЛЬНЫЕ ИСТОЧНИКИ", HTML)
        self.assertIn("не перепаковывает", HTML)

    def test_external_links_open_safely(self):
        for anchor in re.findall(r'<a[^>]+target="_blank"[^>]*>', HTML):
            self.assertIn('rel="noopener noreferrer"', anchor)


if __name__ == "__main__":
    unittest.main(verbosity=2)
