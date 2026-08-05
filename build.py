#!/usr/bin/env python3
"""Stamp shared partials into every page template and write the built site to site/.

site/ is the *only* thing published. It is assembled from an explicit allow list —
the page templates plus ASSETS below — so nothing else in the repo can reach the
public site by accident, no matter what else lands here.
"""

import re
import shutil
from pathlib import Path

SRC        = Path('src')
PARTIALS   = SRC / 'partials'
PAGES      = SRC / 'pages'
OUT        = Path('site')

# Copied into the build output verbatim. Anything not listed here is not published.
ASSETS = ['shared', 'CNAME']

# Pages that live inside a nav dropdown — maps data-page value → data-nav-group value
PAGE_GROUPS = {
    'about-page':          'about',
    'standards':           'about',
    'certifications-page': 'certifications',
    '6005':                'certifications',
    '6010':                'certifications',
    '6015':                'certifications',
    '6020':                'certifications',
    '6030':                'certifications',
    '6035':                'certifications',
    '6040':                'certifications',
    '6050':                'certifications',
    'cert-lookup':         'certifications',
}


def partial(name: str) -> str:
    return (PARTIALS / f'{name}.html').read_text()


def build_nav(page_key: str) -> str:
    nav = partial('nav')

    # Activate the direct link matching this page
    def activate_link(m):
        tag = m.group(0)
        if f'data-nav="{page_key}"' not in tag:
            return tag
        return re.sub(r'class="([^"]*)"', lambda c: f'class="{c.group(1)} is-active"', tag, count=1)

    nav = re.sub(r'<a [^>]*data-nav="[^"]*"[^>]*>', activate_link, nav)

    # Activate the dropdown parent if this page lives inside one
    group = PAGE_GROUPS.get(page_key)
    if group:
        def activate_group(m):
            tag = m.group(0)
            if f'data-nav-group="{group}"' not in tag:
                return tag
            # Use a custom class — not is-active, which Bulma uses to force the dropdown open
            return re.sub(r'class="([^"]*)"', lambda c: f'class="{c.group(1)} is-current-section"', tag, count=1)
        nav = re.sub(r'<div [^>]*data-nav-group="[^"]*"[^>]*>', activate_group, nav)

    return nav


def build_page(src_file: Path) -> None:
    content = src_file.read_text()

    m = re.search(r'<body[^>]*data-page="([^"]*)"', content)
    page_key = m.group(1) if m else ''

    replacements = {
        'header': partial('header'),
        'nav':    build_nav(page_key),
        'footer': partial('footer'),
    }

    for name, html in replacements.items():
        content = content.replace(f'<!-- include:{name} -->', html)

    out = OUT / src_file.name
    out.write_text(content)
    print(f'  {src_file.name}')


def copy_assets() -> None:
    for name in ASSETS:
        src = Path(name)
        if not src.exists():
            raise SystemExit(f'Missing asset: {name}')
        dest = OUT / name
        if src.is_dir():
            shutil.copytree(src, dest)
        else:
            shutil.copy2(src, dest)
        print(f'  {name}')


def main():
    pages = sorted(PAGES.glob('*.html'))
    if not pages:
        print('No pages found in src/pages/')
        return

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()

    print(f'Building {len(pages)} pages into {OUT}/...')
    for page in pages:
        build_page(page)
    print('Copying assets...')
    copy_assets()
    print('Done.')


if __name__ == '__main__':
    main()
