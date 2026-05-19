from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
import os
import json
import re

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

SAVE_FILE = "status.json"

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
        "https://www.ur-net.go.jp/chintai/kanto/tokyo/20_1920.html",

    "鶴見町第二":
        "https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_1770.html",

    "鶴見町":
        "https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_1510.html",

    "ステラ月見ヶ丘":
        "https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_3400.html"
}

# ===== 读取旧状态 =====

if os.path.exists(SAVE_FILE):

    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        old_status = json.load(f)

else:

    old_status = {}

new_status = {}

messages = []

# ===== Selenium设置 =====

options = Options()

options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

# ===== 检查团地 =====

for name, url in DANCHI.items():

    try:

        driver.get(url)

        time.sleep(5)

        html = driver.page_source

        # ===== 检测空室数字 =====

        match = re.search(r"空室\s*(\d+)", html)

        if match:

            count = int(match.group(1))

            if count > 0:

                status = f"有空房（{count}室）"

            else:

                status = "无空房"

        else:

            status = "状态未知"

        print(name, status)

        new_status[name] = status

        old = old_status.get(name)

        # ===== 新出现空房才通知 =====

        if old != status and "有空房" in status:

            msg = f"""
🏠 UR出现空房！

{name}

当前状态：
{status}

{url}
"""

            messages.append(msg)

    except Exception as e:

        print(name, e)

driver.quit()

# ===== Telegram通知 =====

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

    json.dump(
        new_status,
        f,
        ensure_ascii=False,
        indent=2
    )

print("检查完成")
