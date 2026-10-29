# Widget Studio support

## Current workflow

- GitHub HallyAus/widget-studio-support is the source of truth. Use the connected personal account and existing self-hosted GitHub Actions runner. Do not add paid runners or services.
- The public site is https://hallyaus.github.io/widget-studio-support/. Its existing publication branch is github-pages-compatibility; retain branch protection and use a reviewed pull request for updates. Do not move the origin or change Pages settings merely to publish content.
- Keep main and the publication branch reconciled after an accepted release. A commit or passing validation is not proof of publication: read the public page back and compare the approved files.
- Run python3 scripts/verify_static.py and python3 -m unittest discover -s scripts/tests -v. These checks preserve the installed OAuth declaration, privacy and static-site contract. They do not publish the site.

## Installed application compatibility

- Preserve both redirect_uri links, widgetstudio://auth and widgetstudioqa://auth, on the existing HTTPS origin. Installed Home Assistant OAuth clients depend on them.
- This site declares callbacks; it never receives authorization codes, passwords, tokens, household data or form submissions. Keep it static, without scripts, tracking pixels, forms, analytics or a callback collector.
- Preserve the privacy page and support@agenticconsciousness.com.au. Reports remain optional and manually shared; do not send live test messages.
- Store links must identify Widget Studio, App Store ID 6821856563 and Android package com.danielhall.widgetstudio. Link to each store for current availability and release notes instead of treating a development build as publicly available.
- Keep all features free. Approved optional referrals stay disclosed and do not affect access to features.
- Public content describes shipping behaviour. Keep proposed app changes and internal test results in repository release records until verified on the corresponding release.

## Release boundary

This repository deploys only support documentation. App Store uploads, Play uploads, signing, native builds, DNS changes and account changes are separate operations governed by their current project instructions. Record what was verified and leave missing provider/device evidence explicit.

