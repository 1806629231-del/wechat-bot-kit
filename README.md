# 微信 @ 回复机器人 安装包（Grok Bot box 版）

作用：在你的 Grok Bot 电脑（box）上挂一个微信**小号**，群里有人 @ 它时，用大模型回一两句。不群发，也不主动加人。
**先读《封号风险说明.md》**。任何方法都不能保证不被封号。

## 目录
- `install.sh`：总入口，负责安装和检查（`--check`）
- `proxy/`：国内出口代理（手机或电脑当 SOCKS5 出口），含 Windows 版 `install-gost-windows.ps1`
- `box-stack/`：box 上的 Tailscale、proxychains 和守护脚本（box 重置后一键修复）
- `bot/`：回复层，包括 @ 监听、大模型回复、拟人化发送、发送闸（限速和 KILL 开关）、人设模板、数据持久化

## 一步步安装
1. **准备**
   - 一个微信小号，最好养过一阵、实名、有正常好友。不要用主号。
   - 一台放在国内、长期开着的备用安卓手机或电脑，当出口用。
   - 一个 Tailscale 账号。
   - 一个大模型 API Key，任何 OpenAI 兼容接口都行，比如 DeepSeek。
2. **配手机或电脑出口代理**
   - 照 `proxy/README.md` 操作：出口设备装 Tailscale，再开一个带账号密码的 SOCKS5（端口 1080）。
   - Windows 电脑跑 `proxy/install-gost-windows.ps1`。
   - 记下出口设备的 Tailscale IP，它是 100.x 开头的。
3. **在 box 上填代理信息**
   ```bash
   bash install.sh            # 第一次运行会生成 ~/secrets/phone-socks.env，然后退出
   nano ~/secrets/phone-socks.env   # 填 PHONE_SOCKS_HOST/USER/PASS
   bash install.sh            # 正式安装
   ```
   第一次装 Tailscale 时，终端会打印一个登录链接，在浏览器里打开授权即可。
4. **检查**：`bash install.sh --check`。必须看到这一行才算代理通了：`SOCKS exit is in mainland China`。
5. **装微信**
   - 从微信官网下载 Linux 版 .deb，放到 `/workspace/wechat.deb`，然后运行 `sudo apt-get install -y /workspace/wechat.deb`。
   - 启动时**一定要走代理**：`proxychains4 -q wechat`，或者用 box-stack 装好的启动脚本。
6. **扫码登录**：用小号的手机扫码。登录成功后，先关掉微信，运行 `bash /workspace/wechat-bot/wx_persist.sh link`，再重新打开微信。这样以后 box 重置也不用重新扫码。
7. **配大模型和群**：编辑 `/workspace/wechat-bot/.env`，填这几项：
   - BOT_NAME、WATCH_GROUPS
   - LLM_*
   - INPUT_X/INPUT_Y，也就是微信输入框的屏幕坐标。截图量坐标：`DISPLAY=:2 import -window root /tmp/s.png`。

   想换人设，改 `persona.md`。
8. **先 dry_run（只起草，不发送）**
   ```bash
   cd /workspace/wechat-bot
   .venv/bin/python reply.py "测试群" "你好呀"           # 看回复像不像人
   .venv/bin/python mention_watch.py --once --dry        # 看能不能认出 @
   ```
   建议先跑一两天 dry_run，看日志里会回什么。
9. **开发送**：把 `humanize/config.json` 里的 `"SEND_ENABLED"` 改成 `true`，然后运行 `nohup bash watchdog.sh &`。

## 常用命令
| 做什么 | 命令 |
|---|---|
| 全面检查 | `bash install.sh --check` |
| 紧急停发 | `touch /workspace/wechat-bot/humanize/KILL` |
| 恢复发送 | `rm /workspace/wechat-bot/humanize/KILL` |
| 看日志 | `tail -f /workspace/wechat-bot/mention_watch.log` |
| 停监听 | `pkill -f watchdog.sh; pkill -f mention_watch.py` |
| 测一句回复 | `.venv/bin/python reply.py 群名 "内容"` |

## box 重置后怎么恢复
```bash
bash install.sh                                   # 重装 Tailscale/代理/回复层（.env、config 不会被覆盖）
bash /workspace/wechat-bot/wx_persist.sh restore  # 恢复微信、machine-id、登录数据软链
bash install.sh --check
```
做完之后，用代理启动微信。一般不用重新扫码；如果需要扫码，用手机扫一次就行。

## 已知限制（实话说）
- `mention_watch.py` 是 OCR 模板，只能看当前打开的那个会话。要同时盯多个群，得按你自己的屏幕补上切换会话的逻辑，或者改成读本地消息库（本包不含）。
- 发送靠 xdotool 模拟键鼠，存在被识别为外挂的风险，详见风险说明。
