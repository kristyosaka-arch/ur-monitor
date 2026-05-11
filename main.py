import requests
from bs4 import BeautifulSoup
import json
import os

# ========= 配置 =========
URL = "https://www.ur-net.go.jp/chintai/kanto/kanagawa/"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

SAVE_FILE = "rooms.json"

# ========= 抓取 =========
headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(URL, headers=headers)

soup = BeautifulSoup(r.text, "html.parser")

rooms = []

for a in soup.find_all("a"):
    text = a.get_text(strip=True)

    if text and len(text) > 8:
        rooms.append(text)

rooms = list(set(rooms))

# ========= 读取旧数据 =========
if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        old_rooms = json.load(f)
else:
    old_rooms = []

# ========= 对比 =========
new_rooms = [x for x in rooms if x not in old_rooms]

# ========= 通知 =========
if new_rooms:

    message = "UR出现新房源：\n\n"

    for room in new_rooms[:10]:
        message += f"- {room}\n"

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )

# ========= 保存 =========
with open(SAVE_FILE, "w", encoding="utf-8") as f:
    json.dump(rooms, f, ensure_ascii=False, indent=2)

print("完成")
