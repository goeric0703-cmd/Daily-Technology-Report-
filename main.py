import feedparser
import requests
import os
import datetime

# 1. 设置数据源 (这里使用 Hacker News 的免费 RSS 订阅源)
rss_url = "https://news.ycombinator.com/rss"
feed = feedparser.parse(rss_url)

# 2. 整理排版新闻内容
content = "## 🌍 每日全球科技资讯推送\n\n"
for entry in feed.entries[:15]: # 我们只抓取前 15 条最新新闻
    content += f"- [{entry.title}]({entry.link})\n"

# 3. 将内容推送到 GitHub Issues
repo_name = os.environ.get("GITHUB_REPOSITORY")
github_token = os.environ.get("GITHUB_TOKEN")
api_url = f"https://api.github.com/repos/{repo_name}/issues"

headers = {
    "Authorization": f"token {github_token}",
    "Accept": "application/vnd.github.v3+json"
}
data = {
    "title": f"科技资讯日报 - {datetime.date.today()}",
    "body": content
}

# 发送请求
response = requests.post(api_url, headers=headers, json=data)

if response.status_code == 201:
    print("🎉 资讯推送成功！请去 Issues 页面查看。")
else:
    print(f"❌ 推送失败，错误信息：{response.text}")
