#!/usr/bin/env bash
# 总入口。  bash install.sh          安装（代理层 + box 守护 + 回复层）
#           bash install.sh --check  只检查不改动
#   需要先按 README 准备好 ~/secrets/phone-socks.env
set -e; K=$(cd "$(dirname "$0")" && pwd)
SECRETS=${SECRETS:-$HOME/secrets/phone-socks.env}
if [ "$1" = --check ]; then
  bash "$K/box-stack/install.sh" --check --secrets "$SECRETS" || true
  bash "$K/proxy/install.sh" --check --secrets "$SECRETS" || true
  BOT_DIR=${BOT_DIR:-$([ -d /workspace ] && echo /workspace/wechat-bot || echo $HOME/wechat-bot)}
  [ -f "$BOT_DIR/humanize/config.json" ] && echo "PASS 回复层已装 ($BOT_DIR)" || echo "FAIL 回复层未装"
  exit 0; fi
[ -f "$SECRETS" ] || { mkdir -p "$(dirname "$SECRETS")"; install -m 600 "$K/box-stack/.env.example" "$SECRETS"; echo "已生成 $SECRETS，填好代理信息后重跑"; exit 1; }
bash "$K/box-stack/install.sh" --secrets "$SECRETS"
bash "$K/bot/install-bot.sh"
echo "完成。下一步：bash install.sh --check"
