#!/bin/bash
# 守护 mention_watch：挂了就拉起；有 KILL 文件就不拉。每 60s 一次。
D=$(cd "$(dirname "$0")" && pwd); LOG=$D/watchdog.log
while true; do
  if [ -f "$D/humanize/KILL" ]; then echo "$(date '+%F %T') KILL 存在，不启动" >>$LOG
  elif ! pgrep -f "$D/mention_watch.py" >/dev/null; then
    echo "$(date '+%F %T') 拉起 mention_watch" >>$LOG
    nohup "$D/.venv/bin/python" "$D/mention_watch.py" >>"$D/mention_watch.log" 2>&1 &
  fi
  tail -n 1000 $LOG > $LOG.tmp 2>/dev/null && mv $LOG.tmp $LOG; sleep 60
done
