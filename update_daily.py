#!/usr/bin/env python3
"""
OpenClaw Skills Daily 晨间更新脚本
每天早上7:30抓取最新资讯
"""

import subprocess
from datetime import datetime
from pathlib import Path

SITE_DIR = Path("/Users/dingcaozhi/.openclaw/workspace/openclaw-skills-daily")

def fetch_news():
    """使用 Agent Reach 抓取新闻"""
    print("📡 晨间抓取 OpenClaw Skills 资讯...")
    
    sources = [
        ("GitHub OpenClaw", "https://github.com/openclaw/openclaw/commits/main"),
        ("ClawHub", "https://clawhub.com/skills"),
    ]
    
    total = 0
    for name, url in sources:
        result = subprocess.run(
            ["curl", "-s", f"https://r.jina.ai/{url}", "-m", "20"],
            capture_output=True, text=True, timeout=25
        )
        if result.returncode == 0:
            total += 1
            print(f"   ✅ {name}")
    
    print(f"📰 抓取完成: {total} 个源")
    return total

def update_website():
    """更新网站时间戳"""
    index_file = SITE_DIR / "index.html"
    if not index_file.exists():
        return False
    
    content = index_file.read_text(encoding='utf-8')
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 更新时间
    content = content.replace(
        'id="updateTime">',
        f'id="updateTime">{today} '
    )
    
    index_file.write_text(content, encoding='utf-8')
    print(f"✅ 网站更新: {today}")
    return True

def deploy_to_github():
    """部署到 GitHub Pages"""
    try:
        # 提交更新
        subprocess.run(["git", "add", "."], cwd=SITE_DIR, check=True)
        subprocess.run(
            ["git", "commit", "-m", f"Daily update: {datetime.now().strftime('%Y-%m-%d %H:%M')}"],
            cwd=SITE_DIR, capture_output=True
        )
        result = subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=SITE_DIR, capture_output=True, text=True, timeout=60
        )
        
        if result.returncode == 0:
            print("✅ 部署到 GitHub Pages 成功")
            return True
        else:
            print(f"⚠️ Push 可能需要手动处理: {result.stderr[:100]}")
            return False
            
    except Exception as e:
        print(f"❌ 部署失败: {e}")
        return False

def main():
    print(f"\n🌅 OpenClaw Skills Daily")
    print(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏰ 晨间自动更新\n")
    
    fetch_news()
    
    if update_website():
        print("\n🚀 部署中...")
        deploy_to_github()
    
    print("\n✨ 晨间更新完成!\n")

if __name__ == "__main__":
    main()
