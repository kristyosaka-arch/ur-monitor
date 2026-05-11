import requests
import os
import json

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

SAVE_FILE = "status.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

DANCHI = {

    "アーベインビオ川崎":
        "https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_2600.html",

    "フレール川崎大師":
        "https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_4120.html",

    "コンフォール川崎富士見":
        "https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_4020.html",

    "亀戸二丁目":
        "https://www.ur-net.go.jp/chintai/kanto/tokyo/20_1660.html",

    "大島四丁目":
        "https://www.ur-net.go.jp/chintai/kanto/tokyo/20_1780.html",

    "大島六丁目":
        "https://www.ur-net.go.jp/chintai/kanto/tokyo/20_1920.html"
}

# ===== 读取旧状态 =====

if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        old_status = json.load(f)
else:
    old_status = {}

new_status = {}

messages = []

# ===== 检查每个团地 =====

for name, url in DANCHI.items():

    try:

        r = requests.get(url, headers=HEADERS, timeout=20)

        html = r.text

        if "空室なし" in html:
            status = "无空房"

        elif "募集中" in html or "空室あり" in html:
            status = "有空房"

        else:
            status = "状态未知"

        new_status[name] = status

        old = old_status.get(name)

        if old != status:

            msg = f"""
🏠 UR状态变化！

{name}

现在状态：
{status}

{url}
"""

            messages.append(msg)

    except Exception as e:

        messages.append(f"{name} 检查失败: {e}")

# ===== 发送 Telegram =====

for m in messages:

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": m
        }
    )

# ===== 保存状态 =====

with open(SAVE_FILE, "w", encoding="utf-8") as f:
    json.dump(new_status, f, ensure_ascii=False, indent=2)

print("检查完成")
