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

    def test_catalog_contains_all_restored_projects(self):
        for project_id in ("music", "python", "neiro", "drive", "messenger"):
            self.assertRegex(HTML, rf"id:'{project_id}'")

    def test_readme_and_release_history_routes_exist(self):
        self.assertIn("/readme", HTML)
        self.assertIn("/changes", HTML)
        self.assertIn("История изменений", HTML)
        self.assertIn("README / Инструкция", HTML)

    def test_cloudflare_warp_has_official_download_link(self):
        self.assertIn("CLOUDFLARE WARP", HTML)
        self.assertIn("developers.cloudflare.com/cloudflare-one/team-and-resources/devices/cloudflare-one-client/download/", HTML)

    def test_external_links_open_safely(self):
        for anchor in re.findall(r'<a[^>]+target="_blank"[^>]*>', HTML):
            self.assertIn('rel="noopener noreferrer"', anchor)


if __name__ == "__main__":
    unittest.main(verbosity=2)
