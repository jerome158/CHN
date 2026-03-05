#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub镜像源实时搜索脚本
从多个渠道搜索和获取最新的GitHub镜像地址
"""

import re
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime
import os

# 获取脚本所在目录的父目录（项目根目录）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# 搜索关键词和URL模式
SEARCH_PATTERNS = {
    "github加速": [
        r"https?://[a-zA-Z0-9\-\.]+ghp[a-z0-9\-\.]*[a-zA-Z0-9\-\.]+com?",
        r"https?://[a-zA-Z0-9\-\.]+git[a-z0-9\-\.]*[a-zA-Z0-9\-\.]+com?",
        r"https?://[a-zA-Z0-9\-\.]+hub[a-z0-9\-\.]*[a-zA-Z0-9\-\.]+com?",
    ],
    "github镜像": [
        r"https?://[a-zA-Z0-9\-\.]+fastgit[a-z0-9\-\.]*[a-zA-Z0-9\-\.]+",
        r"https?://[a-zA-Z0-9\-\.]+proxy[a-z0-9\-\.]*[a-zA-Z0-9\-\.]+",
    ],
    "ghproxy": [
        r"https?://[a-zA-Z0-9\-\.]*ghproxy[a-zA-Z0-9\-\.]*",
        r"https?://[a-zA-Z0-9\-\.]*mirror[a-zA-Z0-9\-\.]*",
    ]
}

# 可靠的信息源（用于搜索GitHub镜像）
RELIABLE_SOURCES = [
    {
        "name": "GitHub热门仓库搜索",
        "url": "https://github.com/search?q=github+accelerate+mirror&type=repositories",
        "type": "github_search"
    },
    {
        "name": "Awesome GitHub镜像列表",
        "url": "https://github.com/521xueweihan/GitHub-Chinese-Top-Charts",
        "type": "github_repo"
    },
    {
        "name": "V2EX讨论",
        "url": "https://www.v2ex.com/go/github",
        "type": "forum"
    },
    {
        "name": "知乎相关讨论",
        "url": "https://www.zhihu.com/search?q=github%E5%8A%A0%E9%80%9F",
        "type": "search"
    }
]

# 预置的高质量镜像源（作为基础）
BASE_MIRRORS = [
    {
        "name": "GitHub镜像加速 - ghproxy",
        "url": "https://mirror.ghproxy.com",
        "type": "static",
        "prefix": "https://mirror.ghproxy.com/"
    },
    {
        "name": "GitHub镜像加速 - ghproxy.com",
        "url": "https://ghproxy.com",
        "type": "static",
        "prefix": "https://ghproxy.com/"
    },
    {
        "name": "GitHub镜像加速 - GitClone",
        "url": "https://gitclone.com",
        "type": "static",
        "prefix": "https://gitclone.com/github.com/"
    },
    {
        "name": "GitHub镜像加速 - moeyy",
        "url": "https://gh.api.99988866.xyz",
        "type": "static",
        "prefix": "https://gh.api.99988866.xyz/"
    },
    {
        "name": "GitHub镜像加速 - GitProxy",
        "url": "https://ghproxy.net",
        "type": "static",
        "prefix": "https://ghproxy.net/"
    },
    {
        "name": "GitHub镜像加速 - FastGit",
        "url": "https://hub.fastgit.xyz",
        "type": "static",
        "prefix": "https://hub.fastgit.xyz/"
    },
]

def extract_urls_from_text(text, patterns):
    """
    从文本中提取符合模式的URL
    """
    urls = set()
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            # 规范化URL
            if not match.startswith('http://') and not match.startswith('https://'):
                match = 'https://' + match
            # 移除末尾的标点符号
            match = re.sub(r'[.,;!?)]+$', '', match)
            # 确保有协议
            if urlparse(match).scheme:
                urls.add(match)
    return urls

def fetch_page_content(url, timeout=10):
    """
    获取页面内容
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        if response.status_code == 200:
            return response.text
        return None
    except Exception as e:
        print(f"获取页面失败 {url}: {e}")
        return None

def search_github_mirrors():
    """
    从GitHub搜索相关仓库
    """
    mirrors = []
    
    # GitHub API搜索
    search_queries = [
        "github proxy mirror",
        "github加速镜像",
        "ghproxy",
        "fastgit",
        "git加速"
    ]
    
    for query in search_queries:
        try:
            url = f"https://api.github.com/search/repositories?q={query}&sort=updated&per_page=5"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'items' in data:
                    for item in data['items'][:3]:  # 取前3个结果
                        # 从README中提取URL
                        readme_url = f"https://raw.githubusercontent.com/{item['full_name']}/main/README.md"
                        readme_content = fetch_page_content(readme_url)
                        
                        if readme_content:
                            # 提取可能的镜像URL
                            extracted_urls = extract_urls_from_text(
                                readme_content,
                                SEARCH_PATTERNS["github加速"] + SEARCH_PATTERNS["ghproxy"]
                            )
                            
                            for mirror_url in extracted_urls:
                                mirrors.append({
                                    "name": f"GitHub搜索: {item['name']}",
                                    "url": mirror_url,
                                    "source": f"github:{item['full_name']}",
                                    "type": "discovered"
                                })
            
        except Exception as e:
            print(f"GitHub搜索失败 {query}: {e}")
        
        # 避免请求过快
        import time
        time.sleep(1)
    
    return mirrors

def search_from_sources():
    """
    从多个可靠源搜索镜像
    """
    discovered_mirrors = []
    
    # 1. 从GitHub搜索
    print("正在从GitHub搜索...")
    github_mirrors = search_github_mirrors()
    discovered_mirrors.extend(github_mirrors)
    print(f"从GitHub发现 {len(github_mirrors)} 个潜在镜像")
    
    # 2. 从已知的技术博客和文档站点搜索
    tech_sources = [
        "https://zhuanlan.zhihu.com/p/355566649",  # GitHub加速相关文章
        "https://www.cnblogs.com/babosa/p/github-accelerate.html",
    ]
    
    print("正在从技术站点搜索...")
    for source_url in tech_sources:
        content = fetch_page_content(source_url)
        if content:
            # 提取所有URL
            all_patterns = []
            for patterns in SEARCH_PATTERNS.values():
                all_patterns.extend(patterns)
            
            urls = extract_urls_from_text(content, all_patterns)
            for url in urls:
                discovered_mirrors.append({
                    "name": f"技术站点发现: {urlparse(url).netloc}",
                    "url": url,
                    "source": "tech_blog",
                    "type": "discovered"
                })
    
    print(f"从技术站点发现 {len(discovered_mirrors) - len(github_mirrors)} 个潜在镜像")
    
    return discovered_mirrors

def normalize_mirror_url(url):
    """
    规范化镜像URL，确保是完整的前缀格式
    """
    # 移除末尾斜杠
    url = url.rstrip('/')
    
    # 确保有协议
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url
    
    # 添加末尾斜杠（如果不存在）
    if not url.endswith('/'):
        url += '/'
    
    return url

def filter_and_validate_mirrors(discovered_mirrors):
    """
    过滤和验证发现的镜像
    """
    validated = []
    seen_urls = set()
    
    for mirror in discovered_mirrors:
        url = mirror["url"]
        normalized_url = normalize_mirror_url(url)
        
        # 去重
        if normalized_url in seen_urls:
            continue
        seen_urls.add(normalized_url)
        
        # 验证URL格式
        parsed = urlparse(normalized_url)
        if not parsed.netloc:
            continue
        
        # 检查是否包含可疑关键词
        skip_keywords = ['login', 'auth', 'signin', 'register']
        if any(keyword in normalized_url.lower() for keyword in skip_keywords):
            continue
        
        # 构建前缀
        prefix = normalized_url
        if not any(keyword in prefix for keyword in ['github.com', 'gitclone.com']):
            # 如果没有明确的路径模式，添加通用模式
            prefix = normalized_url
        
        validated.append({
            "name": mirror["name"],
            "url": normalized_url,
            "prefix": prefix,
            "type": "discovered",
            "source": mirror.get("source", "unknown"),
            "description": f"通过搜索发现 - 来源: {mirror.get('source', 'unknown')}"
        })
    
    return validated

def main():
    """
    主函数 - 搜索并返回发现的镜像
    """
    print("=" * 60)
    print("GitHub镜像源实时搜索")
    print("=" * 60)
    
    # 1. 获取预置的基础镜像
    print("\n基础镜像源:")
    base_mirrors = BASE_MIRRORS.copy()
    for mirror in base_mirrors:
        print(f"  - {mirror['name']}")
    
    # 2. 搜索发现的镜像
    print("\n开始搜索新的镜像源...")
    discovered_mirrors = search_from_sources()
    
    # 3. 过滤和验证
    print("\n过滤和验证发现的镜像...")
    validated_mirrors = filter_and_validate_mirrors(discovered_mirrors)
    
    # 4. 合并结果
    all_mirrors = base_mirrors + validated_mirrors
    
    print(f"\n总计发现镜像源: {len(all_mirrors)}")
    print(f"  - 基础镜像: {len(base_mirrors)}")
    print(f"  - 搜索发现: {len(validated_mirrors)}")
    
    # 5. 保存到临时文件
    result = {
        "mirrors": all_mirrors,
        "discovery_time": datetime.now().isoformat(),
        "base_count": len(base_mirrors),
        "discovered_count": len(validated_mirrors)
    }
    
    output_file = os.path.join(PROJECT_ROOT, "discovered_mirrors.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n已保存到 {output_file}")
    
    return result

if __name__ == "__main__":
    result = main()
