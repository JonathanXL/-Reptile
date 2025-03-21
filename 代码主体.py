# -*- coding: utf-8 -*-
"""
========================================================
 Author :  JonathanXL
 Date   :  2025/03/11
 Github :  https://github.com/JonathanXL/-Reptile
========================================================
"""

import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

# 代理设置
# 在网站 https://www.kuaidaili.com 中请求一个24小时的免费域名
tunnel = "p761.kdltpspro.com:15818"
username = "t14174260285917"
password = "9twiz468"
proxies = {
    "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {
        "user": username,
        "pwd": password,
        "proxy": tunnel
    },
    "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {
        "user": username,
        "pwd": password,
        "proxy": tunnel
    }
}

# 请求头
# 改headers：在要爬取的页面鼠标右键—检查—网络—刷新网页找到最上面一条点击—拉到最下面找到user-agent
headers = {
    'user-agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
    )
}

# 用于存储成功爬取的结果
results = []

# 记录开始时间
start_time = time.time()


def retry_request(url, max_retries=5):
    """
    对指定 url 发起请求并进行多次重试的函数。

    参数:
        url (str): 需要请求的链接
        max_retries (int): 最大重试次数，默认 5
    返回:
        若请求成功，返回 response 对象；若失败且达到最大重试次数，返回 None
    """
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url, headers=headers, proxies=proxies)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"请求 {url} 失败，第 {retries + 1} 次重试: {e}")
            retries += 1
            time.sleep(2)  # 等待 2 秒后重试

    print(f"请求 {url} 失败，达到最大重试次数。")
    return None

# 主爬取逻辑
for k in range(0, 1000, 20):
    url = 'https://book.douban.com/tag/%E7%AE%A1%E7%90%86'
    response = retry_request(url)
    if response is None:
        # 若该页面连续最大重试次数后仍失败，则跳过
        continue

    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all('div', class_='info')

    # 提取每本书信息
    for i in items:
        try:
            tag = i.find('a')
            name = tag['title']
            link = tag['href']

            # 进入详情页获取短评
            detail_response = retry_request(link)
            if detail_response is None:
                print(f"请求书籍详情页面失败，跳过该书籍: {name}")
                continue

            detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
            comment_section = detail_soup.find('div', class_='comment')

            if comment_section:
                comment = comment_section.find('span', class_='short')
                if comment:
                    results.append([name, comment.text.strip()])
                    print(name, comment.text.strip())
                else:
                    print(f"{name} 未找到短评信息")
            else:
                print(f"{name} 未找到评论区域信息")

        except (AttributeError, KeyError) as e:
            book_name = name if 'name' in locals() else '未知'
            print(f"处理书籍详情页面时出现错误: {e}，书籍名称: {book_name}")

        time.sleep(1)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"爬取完成，所用时间: {elapsed_time} 秒")

# 将结果保存为 Excel 文件
df = pd.DataFrame(results, columns=['书籍名称', '短评内容'])
df.to_excel('douban_books_comments.xlsx', index=False)
