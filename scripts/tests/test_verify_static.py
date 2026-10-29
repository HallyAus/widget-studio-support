import importlib.util
from pathlib import Path
import unittest

SPEC = importlib.util.spec_from_file_location("verify_static", Path(__file__).resolve().parents[1] / "verify_static.py")
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)
FILES = {"index.html", "privacy.html", "icon.png"}
SAFE = '''<!doctype html><html><head><link rel="redirect_uri" href="widgetstudio://auth"><link rel="redirect_uri" href="widgetstudioqa://auth"></head><body id="main"><a href="#main">Home</a><a href="https://apps.apple.com/au/app/id6821856563">iOS</a><a href="https://play.google.com/store/apps/details?id=com.danielhall.widgetstudio">Android</a><p>support@agenticconsciousness.com.au</p></body></html>'''

class StaticContractTests(unittest.TestCase):
    def check(self, text):
        return VERIFY.validate_document(text, "index.html", FILES)
    def test_valid_callback_page(self):
        self.assertEqual([], self.check(SAFE))
    def test_missing_production_callback_is_rejected(self):
        self.assertTrue(self.check(SAFE.replace('href="widgetstudio://auth"', 'href="widgetstudio://changed"')))
    def test_duplicate_callback_does_not_mask_missing_qa(self):
        self.assertTrue(self.check(SAFE.replace("widgetstudioqa://auth", "widgetstudio://auth")))
    def test_forms_scripts_and_iframes_are_rejected(self):
        for tag in ("script", "form", "iframe", "input", "object"):
            with self.subTest(tag=tag):
                self.assertTrue(self.check(SAFE.replace("</body>", f"<{tag}></{tag}></body>")))
    def test_tracking_images_and_handlers_are_rejected(self):
        for content in ('<img src="https://example.com/pixel">', '<img src="icon.png" onload="collect()">'):
            self.assertTrue(self.check(SAFE.replace("</body>", content+"</body>")))
    def test_css_and_javascript_urls_are_rejected(self):
        for content in ('<style>body{background:url(https://example.com/pixel)}</style>', '<a href="javascript:collect()">Go</a>'):
            self.assertTrue(self.check(SAFE.replace("</body>", content+"</body>")))
    def test_missing_local_anchor_is_rejected(self):
        self.assertTrue(self.check(SAFE.replace('href="#main"', 'href="#missing"')))
    def test_wrong_store_identity_is_rejected(self):
        self.assertTrue(self.check(SAFE.replace("id6821856563", "id1234")))
    def test_store_id_in_plain_text_cannot_mask_wrong_destination(self):
        self.assertTrue(self.check(SAFE.replace("apps.apple.com", "example.com") + "id6821856563"))
    def test_implicit_tracking_and_navigation_are_rejected(self):
        for content in ('<img srcset="https://example.com/pixel 2x">', '<a href="https://example.com" ping="https://example.com/track">Go</a>', '<meta http-equiv="refresh" content="0;url=https://example.com">'):
            self.assertTrue(self.check(SAFE.replace("</body>", content+"</body>")))
    def test_css_import_and_svg_external_reference_are_rejected(self):
        for content in ('<style>@import "https://example.com/style";</style>', '<svg><use href="https://example.com/sprite#icon"></use></svg>'):
            self.assertTrue(self.check(SAFE.replace("</body>", content+"</body>")))

if __name__ == "__main__":
    unittest.main()
