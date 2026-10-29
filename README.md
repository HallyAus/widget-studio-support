# Widget Studio support

Static support and privacy pages for Widget Studio: Home Assistant.

## Current workflow

GitHub is the active source of truth. `main` holds the maintainable site; the existing protected `github-pages-compatibility` branch is the publication path to review. Changes to either branch do not establish that Pages has published them. Verify the actual Pages settings, deployment receipt and public response after merging.

The installed OAuth client origin is permanently `https://hallyaus.github.io/widget-studio-support/`. Both installed callback declarations must remain in `index.html`:

- `widgetstudio://auth`
- `widgetstudioqa://auth`

The page is informational. It does not receive authorization codes, tokens, household data or form submissions. It has no scripts, analytics, third-party embeds or remote resources. The existing privacy text and icon are retained. Store and provider pages open only when the visitor follows a link.

## Validation

```sh
python3 -m unittest discover -s scripts/tests -v
python3 scripts/verify_static.py
```

The validator checks the callback declarations, correct store identities, support contact, static/privacy contract, local links and icon signature. Its SHA-256 receipt explicitly says `published: false`; a successful local check is not a deployment receipt.

The GitHub workflow is manual, read-only and targets an existing self-hosted Linux/x64 runner. It never starts native builds or purchases hosted usage. Validate runner availability before dispatch. The old Gitea workflow and its frozen-content allowlist are retired.

## Publication acceptance

1. Review and merge the content through the normal branch protections. Do not force-push, disable protections or change the installed origin.
2. Confirm that Pages is configured for the intended protected branch and that its deployment succeeds for the merged source.
3. Fetch the public root, privacy page and icon; compare their bytes or decoded content to the validated source. Confirm both callback declarations on the HTTPS root.
4. Check phone and desktop layouts, keyboard focus/skip navigation, dark mode, store links, setup steps and disclosure text in a browser.
5. Record the deployment source and public checks. Do not report a live update from a source-only commit.

No iOS or Android binary release is implied by publishing this site.

