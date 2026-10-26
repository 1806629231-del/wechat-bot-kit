# wechat-domestic-exit-proxy – portable pack

Give a box/cloud-hosted Linux WeChat a stable mainland-China exit IP by routing only WeChat through a SOCKS5
proxy on a domestic device reached over Tailscale. Read SKILL.md first (why, lessons, security).

## Contents
- `SKILL.md` – the skill
- `install.sh` – box side: proxychains4 + `/etc/proxychains-wx.conf` + flag-gated `wechat-launch.sh`; `--check`
- `install-gost-windows.ps1` – option B: gost SOCKS5 on a Windows PC (Tailscale-only), `-Check`

## 0. Pick and test the exit device (before installing anything)
On the device itself open https://myip.ipip.net and https://ipinfo.io . It must show a domestic ISP (CN).
Foreign IP ⇒ a VPN app or a side router tunnels it abroad ⇒ choose another device (or add GEOIP-CN direct on the
side router). Keep the device in ONE place on ONE network forever (moving changes the exit IP).

## Option A – spare Android phone (used, working)
1. Tailscale installed, logged into the tailnet, kept alive (lock in Recents; app launch manual; no battery optimization).
2. Install **hev socks5** (open source, MIT): APK from https://github.com/heiher/socks5/releases . Honor/Huawei may ask
   for the Huawei ID password – the owner enters it (or supplies it in a chmod-600 file on the box; type once, never log).
3. Configure: listen address = the phone's **Tailscale IP** (`<PHONE_TS_IP>`), port 1080, auth username/password
   (random, ≥16 chars), start on boot ON, battery optimization OFF, app launch manual (auto/associated/background ON).
4. Confirm the LAN IP and 127.0.0.1 are NOT listening; only the 100.x address.

## Option B – Windows PC (backup)
Run in an elevated PowerShell: `powershell -ExecutionPolicy Bypass -File install-gost-windows.ps1 -User <SOCKS_USER>`
(password auto-generated if omitted). It downloads gost from the official go-gost GitHub releases, binds to the
Tailscale IP, adds a firewall rule limited to 100.64.0.0/10, sets sleep=never, autostarts at boot and checks the
exit country. If it warns "exit is not CN": the PC's gateway goes through a side router/VPN – use a different
device or add GEOIP-CN direct on the router; don't move a PC off the foreign route if the owner needs it.

## Box side
```bash
bash install.sh                       # first run writes ~/secrets/wx-socks.env template (chmod 600) and exits
$EDITOR ~/secrets/wx-socks.env        # PHONE_SOCKS_HOST=<PHONE_TS_IP> PHONE_SOCKS_PORT=1080 PHONE_SOCKS_USER=… PHONE_SOCKS_PASS=…
bash install.sh                       # installs proxychains4, writes /etc/proxychains-wx.conf + ~/bin/wechat-launch.sh
bash install.sh --check               # exit IP is CN & matches device; no-auth / wrong-pass refused; proxychains e2e
# only when the account is unbanned / ready to log in:
touch ~/.wx_proxy_enabled && ~/bin/wechat-launch.sh   # then scan QR with the bot account's own phone
```
Options: `--secrets FILE --conf FILE --launcher FILE --flag FILE --wechat-bin PATH`, `EXPECT_EXIT_IP=…` to pin the exit.

## Migrate
Copy the pack + the secrets file (securely, chmod 600) to the new box, join the tailnet, run `install.sh` and
`--check`; the exit device stays the same, so WeChat keeps seeing the same domestic IP.
