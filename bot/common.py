"""读取 .env 和公共路径。BOT_DIR = 本文件所在目录。"""
import os
D=os.path.dirname(os.path.abspath(__file__))
def load_env():
    p=os.path.join(D,".env")
    if not os.path.exists(p): return
    for l in open(p,encoding="utf-8"):
        l=l.strip()
        if not l or l.startswith("#") or "=" not in l: continue
        k,v=l.split("=",1); v=v.split(" #",1)[0].strip()
        os.environ.setdefault(k.strip(),v)
load_env()
