# Reptile
Python大数据处理之爬虫
# Douban Books Comments Crawler

> **一个基于 Python 的爬虫项目，用于爬取豆瓣“管理”分类的部分图书短评信息。**  
> **作者：JonathanXL**

## 目录
- [项目介绍](#项目介绍)
- [主要功能](#主要功能)
- [环境依赖](#环境依赖)
- [安装与使用](#安装与使用)
- [核心代码简析](#核心代码简析)
- [注意事项](#注意事项)
- [许可证](#许可证)

---

## 项目介绍
本项目通过对[豆瓣读书](https://book.douban.com/)中“管理”分类页面的检索与解析，来获取部分管理学相关书籍的 **短评** 信息，并最终将结果存储到 Excel 文件中。

在代码实现中，主要利用了 Python 的 `requests` 库进行网络请求，配合 `BeautifulSoup` 对 HTML 进行解析和提取。同时，为了保证大规模或频繁请求下的连接稳定性与隐私，本项目使用了付费的 **隧道代理** 服务。

> **提示**：在实际部署时，请确保你有合法的代理授权以及访问豆瓣网的权限，并尽量遵守目标网站的 Robots 协议与相关法律法规。

---

## 主要功能
1. **爬取“管理”分类下的书籍列表**  
2. **进入每本书的详情页面**  
3. **获取并提取第一条短评信息**  
4. **支持断线重试**：若网络请求失败，将自动进行多次重试  
5. **结果保存**：最终以 Excel (`.xlsx`) 文件格式输出

---

## 环境依赖
在使用本项目前，请确保已安装以下依赖：
- **Python 3.7+**（建议 3.8 及以上）
- **requests**：用于发送 HTTP 请求
- **BeautifulSoup4 (bs4)**：用于解析 HTML
- **pandas**：用于表格数据处理及保存

你可以通过以下指令快速安装所需依赖：
```bash
pip install requests beautifulsoup4 pandas
```
## 安装与使用
1. **克隆或下载仓库**
```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```
2. **安装依赖**
```bash
pip install -r requirements.txt
```
3. **修改代理配置信息**
```python
tunnel = "p761.kdltpspro.com:15818"
username = "your-username"
password = "your-password"
```
4. **运行脚本**
```python
python douban_books_crawler.py
```
## 核心代码简析
```python
def retry_request(url, max_retries=5):
    """
    对指定 url 发起请求并进行多次重试的函数。
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
            time.sleep(2)
    return None
```
- retry_request 函数封装了**重试逻辑**，在网络状况不稳定或请求被拒绝时，自动进行多次请求，增强了脚本的可靠性。
- 脚本主逻辑则是：先获取管理分类下的书籍列表，然后遍历每本书的**详情页**提取**短评**。最后将爬取结果写入 Excel 文件。
## 注意事项
- 数据合法性：使用本脚本应遵守豆瓣官方的服务条款；请勿过度或非法抓取，以防对目标网站造成负担或违反网站使用协议。
- 网络环境：脚本依赖代理服务，需确保代理服务可用且账号信息正确。
- 爬取频率：请在脚本中适度调整爬取频率（如增加 time.sleep），避免对目标网站造成影响。
## 许可证
- 本项目仅供个人学习、研究之用。如需商用或二次开发，请遵守 MIT License 或其他指定许可证条款，并确保不侵犯目标网站或其他第三方的合法权益。

- 如有问题或改进建议，欢迎提交 Issue 或发起 Pull Request。
- 感谢你的关注与支持！
