#!/usr/bin/env bash
# 安装回复层到 BOT_DIR（默认 /workspace/wechat-bot，没有 /workspace 就用 ~/wechat-bot）。可重复运行。
set -e
SRC=$(cd "$(dirname "$0")" && pwd)
BOT_DIR=${BOT_DIR:-$([ -d /workspace ] && echo /workspace/wechat-bot || echo $HOME/wechat-bot)}
SUDO=sudo; [ "$(id -u)" = 0 ] && SUDO=
$SUDO apt-get install -y -q python3-venv xdotool xclip imagemagick tesseract-ocr tesseract-ocr-chi-sim >/dev/null
mkdir -p "$BOT_DIR/humanize" "$BOT_DIR/templates"
cp "$SRC"/{common.py,reply.py,send.py,mention_watch.py,wx_persist.sh,watchdog.sh} "$BOT_DIR/"
cp "$SRC"/humanize/{gate.py,human.py,hsend.py} "$BOT_DIR/humanize/"
[ -f "$BOT_DIR/humanize/config.json" ] || cp "$SRC/humanize/config.json" "$BOT_DIR/humanize/"
cp "$SRC/templates/persona.md" "$BOT_DIR/templates/"; [ -f "$BOT_DIR/persona.md" ] || cp "$SRC/templates/persona.md" "$BOT_DIR/persona.md"
[ -f "$BOT_DIR/.env" ] || { install -m 600 "$SRC/.env.example" "$BOT_DIR/.env"; echo "已生成 $BOT_DIR/.env，请填写"; }
[ -d "$BOT_DIR/.venv" ] || python3 -m venv "$BOT_DIR/.venv"
V=$BOT_DIR/.venv; $V/bin/pip install -q humancursor pyautogui python-xlib
SP=$($V/bin/python -c "import site;print(site.getsitepackages()[0])")
if ! $V/bin/python -c "import tkinter" 2>/dev/null && [ -d "$SP/mouseinfo" ] && [ ! -d "$SP/mouseinfo.orig" ]; then
  mv "$SP/mouseinfo" "$SP/mouseinfo.orig"; mkdir -p "$SP/mouseinfo"
  echo "def MouseInfoWindow(*a,**k): raise RuntimeError('stub')" > "$SP/mouseinfo/__init__.py"; fi
chmod +x "$BOT_DIR"/*.sh "$BOT_DIR"/*.py
echo "回复层已装到 $BOT_DIR ；SEND_ENABLED=$(python3 -c "import json;print(json.load(open('$BOT_DIR/humanize/config.json'))['SEND_ENABLED'])")（默认只起草不发送）"
