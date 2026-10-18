"""Verify exact static support/OAuth files without collecting any credentials."""
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import subprocess
from urllib.parse import urlsplit
import zipfile

FILES = ('index.html', 'privacy.html', 'icon.png')
COMPATIBILITY_SOURCE = '3270699ec871359b39ac1c6e79bb488388d7af16'


def git(*args):
    return subprocess.check_output(['git', *args])


class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.redirects = []
        self.active_content = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag in ('script', 'iframe', 'form'):
            self.active_content.append(tag)
        for key in ('href', 'src'):
            if key in values:
                self.links.append(values[key])
        if tag == 'link' and values.get('rel') == 'redirect_uri':
            self.redirects.append(values.get('href'))


def main():
    sha = git('rev-parse', 'HEAD').decode().strip()
    assert re.fullmatch('[0-9a-f]{40}', sha) and os.getenv('GITHUB_SHA') == sha
    assert os.getenv('GITHUB_SERVER_URL') == 'http://192.168.1.130:3000'
    assert os.getenv('GITHUB_REPOSITORY') == 'hallyaus/widget-studio-support'
    assert os.getenv('GITHUB_REF') == 'refs/heads/main'
    assert not git('status', '--porcelain', '--untracked-files=no')
    sources = {name: git('show', sha + ':' + name) for name in FILES}
    for name, content in sources.items():
        # The installed callback origin is frozen. A product-content change
        # requires its separately verified replacement, not a backup push.
        assert content == git('show', COMPATIBILITY_SOURCE + ':' + name), 'Review static publication before changing the compatibility content'
    assert sources['icon.png'].startswith(b'\x89PNG\r\n\x1a\n')
    for name in ('index.html', 'privacy.html'):
        text = sources[name].decode('utf-8')
        assert text.lower().startswith('<!doctype html>')
        assert 'support@agenticconsciousness.com.au' in text
        document = Document()
        document.feed(text)
        assert not document.active_content, 'Support pages must not collect OAuth or household data'
        for link in document.links:
            parsed = urlsplit(link)
            if not parsed.scheme and not parsed.netloc:
                assert parsed.path in ('', *FILES), 'Unresolved relative support link'
            else:
                assert parsed.scheme in ('https', 'mailto', 'widgetstudio', 'widgetstudioqa')
        if name == 'index.html':
            assert set(document.redirects) == {'widgetstudio://auth', 'widgetstudioqa://auth'}
    out = Path('dist')
    out.mkdir(exist_ok=True)
    archive = out / 'widget-studio-support.zip'
    with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED) as zipped:
        for name, content in sources.items():
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            zipped.writestr(info, content)
    with zipfile.ZipFile(archive) as zipped:
        assert zipped.testzip() is None and set(zipped.namelist()) == set(FILES)
        assert all(zipped.read(name) == content for name, content in sources.items())
    receipt = {'repository': 'hallyaus/widget-studio-support', 'source_sha': sha,
               'compatibility_source': COMPATIBILITY_SOURCE, 'run_id': os.getenv('GITHUB_RUN_ID'),
               'static_files_sha256': {name: hashlib.sha256(content).hexdigest() for name, content in sources.items()},
               'archive_sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
               'installed_origin': 'https://hallyaus.github.io/widget-studio-support/',
               'published': False, 'callback_schemes_preserved': True, 'credential_collection': False}
    (out / 'provenance.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(receipt))


if __name__ == '__main__':
    main()
