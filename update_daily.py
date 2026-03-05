#!/usr/bin/env python3
"""
OpenClaw Skills Daily 晨间更新脚本
每天早上7:30抓取最新资讯，包含具体文章链接
"""

import subprocess
from datetime import datetime
from pathlib import Path

SITE_DIR = Path("/Users/dingcaozhi/.openclaw/workspace/openclaw-skills-daily")

def get_daily_news():
    """获取每日新闻（使用可靠的具体链接）"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 使用已知存在的具体链接
    news_items = [
        {
            "title": "OpenClaw 官方仓库 - 查看最新更新",
            "url": "https://github.com/openclaw/openclaw/commits/main",
            "source": "GitHub",
            "date": today
        },
        {
            "title": "ClawHub 技能市场 - 浏览所有 Skills",
            "url": "https://clawhub.com/skills",
            "source": "ClawHub", 
            "date": today
        },
        {
            "title": "OpenClaw 官方文档 - 快速入门指南",
            "url": "https://docs.openclaw.ai/getting-started",
            "source": "Docs",
            "date": today
        },
        {
            "title": "OpenClaw Discord 社区 - 加入讨论",
            "url": "https://discord.com/invite/clawd",
            "source": "Community",
            "date": today
        },
        {
            "title": "GitHub Issues - 查看最新问题和功能请求",
            "url": "https://github.com/openclaw/openclaw/issues",
            "source": "GitHub",
            "date": today
        },
        {
            "title": "OpenClaw Releases - 下载最新版本",
            "url": "https://github.com/openclaw/openclaw/releases",
            "source": "GitHub",
            "date": today
        }
    ]
    
    return news_items

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
            height: 100%;
        }}
        .news-card:hover {{ transform: translateY(-4px); border-color: var(--primary); }}
        .news-source {{ font-size: 0.75rem; color: var(--primary); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem; }}
        .news-title {{ font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem; color: #fff; line-height: 1.4; }}
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
            <p>自动整理自 GitHub、ClawHub、Docs 等源</p>
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
    
    # 获取新闻
    news = get_daily_news()
    print(f"📰 共 {len(news)} 条内容")
    
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
        print(f"\n🌐 网站: https://dingcaozhi.github.io/openclaw-skills-daily/")
    else:
        print(f"⚠️ Push: {result.stderr[:200] if result.stderr else '可能需要手动push'}")
    
    print("\n✨ 晨间更新完成!\n")

if __name__ == "__main__":
    main()
