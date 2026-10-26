#!/usr/bin/env python3
"""用大模型生成一句回复。用法: reply.py "群名" "对方说的话" """
import os, sys, json, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import common
sys.path.insert(0, os.path.join(common.D,"humanize")); import gate
def persona():
    p=os.path.join(common.D,"persona.md")
    if not os.path.exists(p): p=os.path.join(common.D,"templates","persona.md")
    return open(p,encoding="utf-8").read().replace("{BOT_NAME}",os.environ.get("BOT_NAME","机器人"))
def reply(chat, text):
    body={"model":os.environ.get("LLM_MODEL","deepseek-chat"),"temperature":0.8,"max_tokens":200,
          "messages":[{"role":"system","content":persona()+f"\n【场景】微信群「{chat}」里有人 @ 你。直接给最终回复。"},
                      {"role":"user","content":text}]}
    req=urllib.request.Request(os.environ["LLM_BASE_URL"].rstrip("/")+"/chat/completions",data=json.dumps(body).encode(),
        headers={"Content-Type":"application/json","Authorization":"Bearer "+os.environ["LLM_API_KEY"]})
    r=json.load(urllib.request.urlopen(req,timeout=60))["choices"][0]["message"]["content"]
    return gate.trim(r)
if __name__=="__main__": print(reply(sys.argv[1], sys.argv[2]))
