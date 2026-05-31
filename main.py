from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import requests
import os
import json

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

SAVE_FILE = "status.json"

DANCHI = {

    "川崎旭町ハイツ":
        "https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_2600.html",

    "コンフォール川崎富士見":
        "https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_4120.html",

    "アーベインビオ川崎":
        "https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_4020.html",

    "龟户二丁目":
        "https://www.ur-net.go.jp/chintai/kanto/tokyo/20_1660.html",

    "大岛四丁目":
        "https://www.ur-net.go.jp/chintai/kanto/tokyo/20_1780.html",

    "大岛六丁目":
        "https://www.ur-net.go.jp/chintai/kanto/tokyo/20_1920.html",

    "鹤见町第二":
        "https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_1770.html",

    "鹤见町":
        "https://www.ur-net.go.jp/chintai/kanto/kanagawa/40_1510.html"

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

        # ===== 等待网页加载 =====

        try:

            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located(
                    (By.TAG_NAME, "body")
                )
            )

        except:
            pass

        time.sleep(5)

        # ===== 读取网页真实显示文字 =====

        html = driver.find_element(By.TAG_NAME, "body").text

        print(name)
        print(html)

        # ===== 判断有无房 =====

        if "空室は前日以前の状況です" in html:

            status = "有空房"

        elif "ご案内できるお部屋がございません" in html:

            status = "无空房"

        else:

            status = "状态未知"

        print(name, status)

        new_status[name] = status

        old = old_status.get(name)

        # ===== 新出现空房才通知 =====

        if old != status and status == "有空房":

            msg = f"""
🏠 UR出现空房！

{name}

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
