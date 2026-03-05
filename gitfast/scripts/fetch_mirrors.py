#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub镜像加速地址提取脚本
从多个可靠来源获取GitHub镜像地址，支持实时网络搜索
"""

import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import time
import os
import sys

# 获取脚本所在目录的父目录（项目根目录）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# 镜像源配置
MIRROR_SOURCES = [
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
    {
        "name": "GitHub镜像加速 - Gitee镜像",
        "url": "https://gitee.com/mirrors",
        "type": "static",
        "prefix": "https://gitee.com/"
    },
]

# 测试URL（用于验证镜像是否可用）
TEST_URL = "https://github.com/torvalds/linux.git"

def enable_realtime_search():
    """
    是否启用实时搜索功能
    """
    # 通过环境变量控制是否启用搜索
    return os.getenv('ENABLE_REALTIME_SEARCH', 'true').lower() == 'true'

def load_discovered_mirrors():
    """
    加载通过搜索发现的镜像
    """
    discovered_file = os.path.join(PROJECT_ROOT, "discovered_mirrors.json")
    if os.path.exists(discovered_file):
        try:
            with open(discovered_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("mirrors", [])
        except Exception as e:
            print(f"加载发现的镜像失败: {e}")
    return []

def run_realtime_search():
    """
    运行实时搜索
    """
    try:
        # 导入搜索模块
        import sys
        script_dir = os.path.dirname(os.path.abspath(__file__))
        search_script = os.path.join(script_dir, "search_mirrors.py")
        
        if os.path.exists(search_script):
            print("正在运行实时搜索...")
            # 动态导入和执行
            import subprocess
            result = subprocess.run(
                [sys.executable, search_script],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print("搜索完成")
                return load_discovered_mirrors()
            else:
                print(f"搜索执行失败: {result.stderr}")
                return []
    except Exception as e:
        print(f"实时搜索出错: {e}")
    return []

def get_all_mirrors():
    """
    获取所有镜像源（包括预置和搜索发现的）
    """
    mirrors = MIRROR_SOURCES.copy()
    
    # 如果启用了实时搜索，加载发现的镜像
    if enable_realtime_search():
        print("\n检查是否有新发现的镜像...")
        discovered = load_discovered_mirrors()
        
        # 如果没有发现的镜像或需要重新搜索
        if not discovered and enable_realtime_search():
            discovered = run_realtime_search()
        
        # 合并发现的镜像
        if discovered:
            seen_prefixes = {m["prefix"] for m in mirrors}
            
            for new_mirror in discovered:
                if new_mirror.get("prefix") not in seen_prefixes:
                    mirrors.append(new_mirror)
                    seen_prefixes.add(new_mirror.get("prefix"))
                    print(f"  + 发现新镜像: {new_mirror['name']}")
    
    return mirrors

def check_mirror_availability(prefix):
    """
    检查镜像地址是否可用
    
    Args:
        prefix: 镜像前缀
        
    Returns:
        dict: 包含状态和响应时间
    """
    test_url = prefix + "torvalds/linux.git"
    
    try:
        start_time = time.time()
        response = requests.head(test_url, timeout=10, allow_redirects=True)
        end_time = time.time()
        
        response_time = round((end_time - start_time) * 1000, 2)  # 毫秒
        
        if response.status_code in [200, 301, 302]:
            return {
                "available": True,
                "status_code": response.status_code,
                "response_time": response_time,
                "message": "可用"
            }
        else:
            return {
                "available": False,
                "status_code": response.status_code,
                "response_time": response_time,
                "message": f"状态码: {response.status_code}"
            }
    except requests.exceptions.Timeout:
        return {
            "available": False,
            "status_code": None,
            "response_time": None,
            "message": "超时"
        }
    except Exception as e:
        return {
            "available": False,
            "status_code": None,
            "response_time": None,
            "message": str(e)[:50]
        }

def fetch_mirrors():
    """
    从各个源获取镜像地址并测试可用性
    """
    # 获取所有镜像源（包括搜索发现的）
    all_mirrors = get_all_mirrors()
    
    mirrors_data = {
        "mirrors": [],
        "last_updated": datetime.now().isoformat(),
        "total_count": len(all_mirrors),
        "available_count": 0,
        "static_count": len(MIRROR_SOURCES),
        "discovered_count": len(all_mirrors) - len(MIRROR_SOURCES)
    }
    
    print(f"\n开始检查 {len(all_mirrors)} 个镜像源...")
    print(f"  - 预置镜像: {mirrors_data['static_count']}")
    print(f"  - 发现镜像: {mirrors_data['discovered_count']}")
    print()
    
    for source in all_mirrors:
        print(f"正在检查: {source['name']}")
        
        mirror_info = {
            "name": source["name"],
            "url": source["url"],
            "prefix": source["prefix"],
            "type": source.get("type", "static"),
            "source": source.get("source", "unknown"),
            "description": source.get("description", f"{source['name']} - GitHub加速镜像")
        }
        
        # 检查可用性
        availability = check_mirror_availability(source["prefix"])
        mirror_info.update(availability)
        
        if availability["available"]:
            mirrors_data["available_count"] += 1
            print(f"  ✓ 可用 - 响应时间: {availability['response_time']}ms")
        else:
            print(f"  ✗ 不可用 - {availability['message']}")
        
        mirrors_data["mirrors"].append(mirror_info)
        
        # 避免请求过快
        time.sleep(0.5)
    
    # 按可用性和响应时间排序
    mirrors_data["mirrors"].sort(key=lambda x: (
        not x["available"],
        x["response_time"] if x["response_time"] else float('inf'),
        x["type"] == "discovered"  # 优先显示预置的
    ))
    
    return mirrors_data

def save_mirrors(data, filename="mirrors.json"):
    """
    保存镜像数据到JSON文件
    """
    # 确保使用项目根目录的完整路径
    if not os.path.isabs(filename):
        filename = os.path.join(PROJECT_ROOT, filename)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*60}")
    print(f"镜像数据已保存到 {filename}")
    print(f"总计: {data['total_count']} 个")
    print(f"可用: {data['available_count']} 个")
    if 'static_count' in data:
        print(f"预置: {data['static_count']} 个")
        print(f"发现: {data['discovered_count']} 个")

def main():
    """
    主函数
    """
    print("=" * 60)
    print("GitHub镜像加速地址提取工具")
    if enable_realtime_search():
        print("实时搜索功能: 已启用")
    else:
        print("实时搜索功能: 已禁用")
    print("=" * 60)
    
    # 获取镜像数据
    mirrors_data = fetch_mirrors()
    
    # 保存数据
    save_mirrors(mirrors_data)
    
    # 输出可用镜像列表
    print("\n可用的镜像地址:")
    print("-" * 60)
    available_mirrors = [m for m in mirrors_data["mirrors"] if m["available"]]
    for mirror in available_mirrors:
        type_indicator = "🔍" if mirror.get("type") == "discovered" else "⭐"
        print(f"{type_indicator} {mirror['name']}")
        print(f"  前缀: {mirror['prefix']}")
        print(f"  响应时间: {mirror['response_time']}ms")
        if mirror.get("source") and mirror.get("source") != "unknown":
            print(f"  来源: {mirror['source']}")
        print()
    
    unavailable_mirrors = [m for m in mirrors_data["mirrors"] if not m["available"]]
    if unavailable_mirrors:
        print("不可用的镜像地址:")
        print("-" * 60)
        for mirror in unavailable_mirrors:
            print(f"✗ {mirror['name']}")
            print(f"  原因: {mirror['message']}")
            print()
    
    print("=" * 60)
    print("完成!")
    
    # 清理临时文件
    discovered_file = os.path.join(PROJECT_ROOT, "discovered_mirrors.json")
    if os.path.exists(discovered_file):
        try:
            os.remove(discovered_file)
            print("临时文件已清理")
        except:
            pass

if __name__ == "__main__":
    main()
