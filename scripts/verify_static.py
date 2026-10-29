"""Validate installed OAuth declarations and static support content, without network access."""
from html.parser import HTMLParser
from pathlib import Path
import argparse
import hashlib
import json
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
CALLBACKS = {"widgetstudio://auth", "widgetstudioqa://auth"}
SUPPORT_EMAIL = "support@agenticconsciousness.com.au"
FORBIDDEN = {"script", "iframe", "form", "input", "textarea", "object", "embed"}

class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.redirects, self.links, self.errors = [], [], []
        self.ids = set()
    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag in FORBIDDEN:
            self.errors.append(f"Active or collecting content: {tag}")
        if any(key.lower().startswith("on") for key, _ in attrs):
            self.errors.append("Inline event handlers are not allowed")
        if any(key.lower() in {"srcset", "ping", "poster", "background"} for key, _ in attrs):
            self.errors.append("Implicit resource loads are not allowed")
        if tag == "base" or (tag == "meta" and values.get("http-equiv", "").lower() == "refresh"):
            self.errors.append("Automatic navigation is not allowed")
        if values.get("id"):
            if values["id"] in self.ids:
                self.errors.append("Duplicate element ID")
            self.ids.add(values["id"])
        if tag == "link" and values.get("rel") == "redirect_uri":
            self.redirects.append(values.get("href"))
        for attribute in ("href", "src"):
            if attribute in values:
                self.links.append((tag, attribute, values[attribute]))

def validate_document(text, name, files):
    errors = []
    if not text.lstrip().lower().startswith("<!doctype html>"):
        errors.append("Missing HTML doctype")
    if SUPPORT_EMAIL not in text:
        errors.append("Missing support contact")
    if re.search(r"url\s*\(|@import\b", text, re.I):
        errors.append("CSS resource loads are not allowed")
    document = Document()
    document.feed(text)
    errors.extend(document.errors)
    for tag, attribute, link in document.links:
        parsed = urlsplit(link)
        if parsed.scheme in ("widgetstudio", "widgetstudioqa"):
            if tag != "link" or link not in CALLBACKS:
                errors.append("Unexpected application callback")
        elif parsed.scheme:
            if parsed.scheme not in ("https", "mailto") or parsed.username or parsed.password:
                errors.append("Unsafe external link")
            if attribute == "src" or tag != "a":
                errors.append("External resource loads are not allowed")
        elif parsed.netloc:
            errors.append("Protocol-relative links are not allowed")
        else:
            if parsed.path and parsed.path not in files:
                errors.append(f"Missing local file: {parsed.path}")
            if not parsed.path and parsed.fragment and parsed.fragment not in document.ids:
                errors.append(f"Missing anchor: {parsed.fragment}")
    if name == "index.html":
        if len(document.redirects) != 2 or set(document.redirects) != CALLBACKS:
            errors.append("Installed OAuth callback declarations changed")
        stores = [urlsplit(link) for tag, attribute, link in document.links if tag == "a" and attribute == "href"]
        expected_stores = (
            any(url.scheme == "https" and url.hostname == "apps.apple.com" and url.path.rstrip("/").endswith("/id6821856563") for url in stores),
            any(url.scheme == "https" and url.hostname == "play.google.com" and url.path == "/store/apps/details" and "id=com.danielhall.widgetstudio" in url.query.split("&") for url in stores),
        )
        for correct_store in expected_stores:
            if not correct_store:
                errors.append("Missing correct store link")
        if "Public store releases are being prepared" in text:
            errors.append("Obsolete launch status")
    return errors

def verify(root=ROOT):
    files = {"index.html", "privacy.html", "icon.png"}
    errors = []
    receipt = {"files": {}, "oauth_callbacks_preserved": False, "published": False}
    for name in sorted(files):
        path = root / name
        if not path.is_file():
            errors.append(f"Missing file: {name}")
            continue
        data = path.read_bytes()
        receipt["files"][name] = hashlib.sha256(data).hexdigest()
        if name.endswith(".html"):
            errors.extend(f"{name}: {error}" for error in validate_document(data.decode("utf-8"), name, files))
        elif not data.startswith(b"\x89PNG\r\n\x1a\n"):
            errors.append("Invalid icon PNG")
    receipt["oauth_callbacks_preserved"] = not errors
    return errors, receipt

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    errors, receipt = verify(args.root)
    if errors:
        raise SystemExit("\n".join(errors))
    print(json.dumps(receipt, indent=2))

if __name__ == "__main__":
    main()
