import requests as rq
from bs4 import BeautifulSoup
import os
import time


page_url = "http://www.shmeea.edu.cn/page/08000/20200806/14399.html"
ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.61"
headers = {
    "User-Agent": ua
}
key =  os.environ["KEY"]


def get_sleep_time():
    # 查询间隔
    date = time.localtime(time.time())[2]
    date_table = {
        20: 5 * 60,
        21: 4 * 60,
        22: 3 * 60,
        23: 2 * 60
    }
    if not date == 24:
        return date_table[date]
    else:
        hour = time.localtime(time.time())[3]
        if hour >= 12:
            return 45
        else:
            return 60


def notify(title, text):
    payload = {
        "text": title,
        "desp": text
    }
    u = f"https://sc.ftqq.com/{key}.send"
    rq.get(u, params=payload)


def query():
    try:
        resp = rq.get(page_url, headers=headers)
    except:
        notify("???","")
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text)
    tr = soup.findAll("tr")[6]
    if len(tr.findAll("a")) == 0:
        # 未开通
        print(time.strftime("[%m.%d] %H:%M:%S "), end="")
        print("暂未开通")
    else:
        # 已开通
        a = tr.findAll("a")
        markdown = ""
        for x in a:
            text = x.string
            url = x.attrs["href"]
            markdown_url = f"[{text}]({url})"
            markdown += markdown_url
            markdown += "  \n"
        print("已发送")
        print(markdown)
        notify("!!!", markdown)
        import sys
        sys.exit()


print(f"校时，现在是 {time.localtime(time.time())[3]}:{time.localtime(time.time())[4]}")
while True:
    query()
    time.sleep(get_sleep_time())