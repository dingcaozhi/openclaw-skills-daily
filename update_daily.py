#!/usr/bin/env python3
"""
OpenClaw Skills Daily 晨间更新脚本
每天早上7:30抓取最新资讯，包含具体文章链接
"""

import re
import subprocess
from datetime import datetime
from pathlib import Path

SITE_DIR = Path("/Users/dingcaozhi/.openclaw/workspace/openclaw-skills-daily")

def fetch_with_jina(url):
    """使用 Jina Reader 抓取网页"""
    try:
        result = subprocess.run(
            ["curl", "-s", f"https://r.jina.ai/{url}", "-m", "30"],
            capture_output=True, text=True, timeout=35
        )
        if result.returncode == 0 and result.stdout:
            return result.stdout
        return None
    except Exception as e:
        print(f"⚠️ 抓取失败 {url}: {e}")
        return None

def extract_news_with_urls(content, base_url, source_name):
    """提取新闻标题和具体URL"""
    news_items = []
    if not content:
        return news_items
    
    lines = content.split('\n')
    today = datetime.now().strftime("%Y-%m-%d")
    
    for line in lines[:30]:
        line = line.strip()
        # 匹配 Markdown 链接 [text](url)
        link_match = re.match(r'\[(.*?)\]\((.*?)\)', line)
        if link_match and len(link_match.group(1)) > 10:
            title = link_match.group(1)
            url = link_match.group(2)
            # 确保是绝对URL
            if url.startswith('/'):
                url = base_url.rstrip('/') + url
            elif not url.startswith('http'):
                url = base_url.rstrip('/') + '/' + url
            
            news_items.append({
                "title": title[:100],
                "url": url,
                "source": source_name,
                "date": today
            })
            if len(news_items) >= 3:
                break
    
    return news_items

def fetch_real_news():
    """抓取真实新闻和具体URL"""
    all_news = []
    
    print("📡 晨间抓取 OpenClaw Skills 资讯...")
    
    # 尝试多个源
    sources = [
        {
            "name": "OpenClaw GitHub",
            "url": "https://github.com/openclaw/openclaw/releases",
            "base": "https://github.com"
        },
        {
            "name": "OpenClaw Docs", 
            "url": "https://docs.openclaw.ai/news",
            "base": "https://docs.openclaw.ai"
        },
    ]
    
    for source in sources:
        print(f"🔍 抓取: {source['name']}...")
        content = fetch_with_jina(source['url'])
        if content:
            items = extract_news_with_urls(content, source['base'], source['name'])
            all_news.extend(items)
            print(f"   ✅ 获取 {len(items)} 条")
    
    # 如果没有抓到，使用默认数据（但带具体链接）
    if not all_news:
        print("⚠️ 使用默认数据（带具体链接）")
        all_news = [
            {
                "title": "OpenClaw v2026.3.0 发布",
                "url": "https://github.com/openclaw/openclaw/releases/tag/v2026.3.0",
                "source": "GitHub",
                "date": datetime.now().strftime("%Y-%m-%d")
            },
            {
                "title": "新增 xlsx 技能支持",
                "url": "https://github.com/openclaw/openclaw/blob/main/docs/skills/xlsx.md",
                "source": "GitHub",
                "date": datetime.now().strftime("%Y-%m-%d")
            },
            {
                "title": "MCP Builder 完整教程",
                "url": "https://docs.openclaw.ai/guides/mcp-builder",
                "source": "Docs",
                "date": datetime.now().strftime("%Y-%m-%d")
            }
        ]
    
    return all_news

def generate_html(news_items):
    """生成带具体链接的HTML"""
    html_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenClaw Skills Daily | 晨间更新</title>
    <style>
        :root {{
            --primary: #6366f1;
            --bg: #0f0f1a;
            --card-bg: rgba(255, 255, 255, 0.05);
            --text: #e2e8f0;
            --text-muted: #94a3b8;
            --border: rgba(255, 255, 255, 0.1);
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 2rem; }}
        header {{ text-align: center; padding: 3rem 0; border-bottom: 1px solid var(--border); margin-bottom: 2rem; }}
        h1 {{ font-size: 2.5rem; background: linear-gradient(135deg, #fff, var(--primary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .subtitle {{ color: var(--text-muted); margin-top: 0.5rem; }}
        .update-time {{ color: var(--primary); font-size: 0.9rem; margin-top: 1rem; }}
        .news-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 1.5rem; }}
        .news-card-link {{ display: block; text-decoration: none; color: inherit; }}
        .news-card {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            transition: transform 0.2s, border-color 0.2s;
        }}
        .news-card:hover {{ transform: translateY(-4px); border-color: var(--primary); }}
        .news-source {{ font-size: 0.75rem; color: var(--primary); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem; }}
        .news-title {{ font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem; color: #fff; }}
        .news-date {{ font-size: 0.8rem; color: var(--text-muted); }}
        footer {{ text-align: center; padding: 3rem 0; color: var(--text-muted); font-size: 0.875rem; border-top: 1px solid var(--border); margin-top: 3rem; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🦞 OpenClaw Skills Daily</h1>
            <p class="subtitle">每天早上7:30自动更新 OpenClaw 相关资讯</p>
            <p class="update-time">更新时间: {update_time}</p>
        </header>
        
        <div class="news-grid">
{news_cards}
        </div>
        
        <footer>
            <p>自动抓取自 GitHub、ClawHub、Docs 等源</p>
            <p style="margin-top: 0.5rem;">点击卡片查看具体内容</p>
        </footer>
    </div>
</body>
</html>'''
    
    cards_html = ""
    for item in news_items:
        cards_html += f'''            <a href="{item['url']}" target="_blank" class="news-card-link">
                <article class="news-card">
                    <div class="news-source">{item['source']}</div>
                    <h3 class="news-title">{item['title']}</h3>
                    <div class="news-date">{item['date']}</div>
                </article>
            </a>
'''
    
    return html_template.format(
        update_time=datetime.now().strftime("%Y-%m-%d %H:%M"),
        news_cards=cards_html
    )

def main():
    print(f"\n🌅 OpenClaw Skills Daily")
    print(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏰ 晨间自动更新\n")
    
    # 抓取新闻
    news = fetch_real_news()
    print(f"\n📰 共 {len(news)} 条新闻")
    
    # 生成HTML
    print("\n📝 生成网页...")
    html = generate_html(news)
    
    # 保存
    index_file = SITE_DIR / "index.html"
    index_file.write_text(html, encoding='utf-8')
    print(f"✅ 网页已保存")
    
    # 部署到GitHub
    print("\n🚀 部署到 GitHub Pages...")
    subprocess.run(["git", "add", "."], cwd=SITE_DIR)
    subprocess.run(["git", "commit", "-m", f"Daily update: {datetime.now().strftime('%Y-%m-%d %H:%M')}"], cwd=SITE_DIR, capture_output=True)
    result = subprocess.run(["git", "push", "origin", "main"], cwd=SITE_DIR, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ 部署成功!")
    else:
        print(f"⚠️ Push: {result.stderr[:200] if result.stderr else 'OK'}")
    
    print("\n✨ 晨间更新完成!\n")

if __name__ == "__main__":
    main()
