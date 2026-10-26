#!/usr/bin/env python3
"""@ 监听模板（OCR 版，最通用）：定时截微信窗口 → tesseract 识别 → 看到「@BOT_NAME」就生成回复并走 send.py。
用法: mention_watch.py [--once] [--interval 8] [--dry]
限制：OCR 只能看当前打开的会话；多群监听需要你按自己的屏幕补「切换会话」逻辑。
更稳的做法是读本地消息库（需自己解密，此模板不包含）。"""
import os, sys, time, hashlib, subprocess as sp, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import common, reply, send
sys.path.insert(0, os.path.join(common.D,"humanize")); import gate
NAME=os.environ.get("BOT_NAME",""); GROUPS=[g for g in os.environ.get("WATCH_GROUPS","").split(",") if g]
SEEN=os.path.join(common.D,"seen.json")
def ocr():
    env=dict(os.environ,DISPLAY=os.environ.get("WX_DISPLAY",":2")); png="/tmp/wx_watch.png"
    sp.run(["import","-window","root",png],env=env,check=True)
    return sp.run(["tesseract",png,"-","-l","chi_sim+eng"],capture_output=True,text=True).stdout
def current_chat(txt):
    for g in GROUPS:
        if g in txt: return g
def tick(dry):
    txt=ocr(); chat=current_chat(txt)
    if not chat or not NAME: return
    seen=set(json.load(open(SEEN))) if os.path.exists(SEEN) else set()
    for line in txt.splitlines():
        if "@"+NAME in line.replace(" ",""):
            h=hashlib.md5((chat+line).encode()).hexdigest()
            if h in seen: continue
            seen.add(h); json.dump(list(seen)[-500:],open(SEEN,"w"))
            q=re.sub(r"@\S+","",line).strip() or "（有人@你）"
            gate.mention_jitter(); r=reply.reply(chat,q); send.main(chat,r,dry=dry)
if __name__=="__main__":
    a=sys.argv; dry="--dry" in a or not gate.send_enabled()
    iv=int(a[a.index("--interval")+1]) if "--interval" in a else 8
    print("mention_watch start, dry=",dry)
    while True:
        try: tick(dry)
        except Exception as e: print("err",e)
        if "--once" in a: break
        time.sleep(iv)
