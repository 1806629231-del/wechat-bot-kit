#!/usr/bin/env python3
"""拟人化发一条消息到当前已打开的微信会话（必须先过发送闸）。
用法: send.py "会话名" "内容" [--dry]
做法：激活微信窗口 → 用 HumanCursor 弧线点输入框 → 思考停顿 → 分段粘贴 → 停顿后回车。
注意：本模板假设你已手动/用 Ctrl+F 切到该会话；切会话逻辑因分辨率不同，请自行补充。"""
import os, sys, subprocess as sp, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import common
sys.path.insert(0, os.path.join(common.D,"humanize")); import gate, human
def main(chat, msg, dry=False, is_group=True):
    msg=gate.trim(msg); ok,why=gate.check(chat,msg,is_group)
    if not ok: print("BLOCKED",why); return 2
    if dry or not gate.send_enabled(): print("DRY_RUN would send:",chat,"|",msg); return 0
    os.environ["DISPLAY"]=os.environ.get("WX_DISPLAY",":2")
    w=sp.run(["xdotool","search","--name","微信|WeChat"],capture_output=True,text=True).stdout.split()
    if not w: print("微信窗口没找到"); return 3
    sp.run(["xdotool","windowactivate","--sync",w[-1]])
    human.click(int(os.environ["INPUT_X"]),int(os.environ["INPUT_Y"]))
    human.think(msg); human.paste_chunks(msg); human.pre_enter()
    sp.run(["xdotool","key","Return"]); gate.record(chat); print("SENT",chat); return 0
if __name__=="__main__":
    a=[x for x in sys.argv[1:] if x!="--dry"]; sys.exit(main(a[0],a[1],"--dry" in sys.argv))
