# Widget Studio support and installed OAuth compatibility

Primary source is private VM300 hallyaus/widget-studio-support, SSH2222.
Keep public GitHub as identical recovery with Actions disabled. Ordinary
recovery pushes to main must not build or deploy.

Installed applications use https://hallyaus.github.io/widget-studio-support/
as their OAuth client-origin/callback declaration. Preserve its HTTPS address,
both widgetstudio://auth and widgetstudioqa://auth declarations, support email,
privacy text and icon. The static site does not receive authorization codes,
tokens, household data or form submissions. Never add a callback collector.

The intended GitHub Pages source is a frozen github-pages-compatibility branch
at3270699ec871359b39ac1c6e79bb488388d7af16. Verify its actual Pages settings,
successful build and exact public bytes before relying on this. Main recovery
pushes must then remain inert. Do not move or delete that compatibility branch
as routine recovery. Existing public issues are another compatibility consumer
and are preserved; support email is support@agenticconsciousness.com.au.

Gitea CI verifies and packages the same three static files and exact-source
receipt. It deliberately rejects content drift until the publication route and
installed-origin compatibility have been separately reviewed. Candidate
packaging does not establish a new deployment or full GitHub independence.
Any future hosting/domain change must preserve installed clients, verify the
personal provider account, keep Cloudflare authoritative DNS and update the
privacy statement accurately. No app-store/Apple release is part of this route.
