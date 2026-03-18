#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Pages页面生成脚本
根据镜像数据生成静态HTML页面
"""

import json
from datetime import datetime
import os

# 获取脚本所在目录的父目录（项目根目录）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

def load_mirrors(filename="mirrors.json"):
    """
    加载镜像数据
    """
    # 确保使用项目根目录的完整路径
    if not os.path.isabs(filename):
        filename = os.path.join(PROJECT_ROOT, filename)
    
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def deduplicate_mirrors(mirrors):
    """
    去重:保留响应时间最短的镜像
    """
    # 使用字典去重,key为prefix,值为镜像对象
    mirror_dict = {}
    for mirror in mirrors:
        prefix = mirror.get("prefix", "")
        if prefix:
            # 如果prefix已存在,保留响应时间更短的
            if prefix not in mirror_dict:
                mirror_dict[prefix] = mirror
            else:
                existing = mirror_dict[prefix]
                existing_time = existing.get("response_time")
                new_time = mirror.get("response_time")

                # 处理 None 值:有值的优先,都为 None 时保留第一个
                if existing_time is None and new_time is not None:
                    mirror_dict[prefix] = mirror
                elif existing_time is not None and new_time is not None:
                    if new_time < existing_time:
                        mirror_dict[prefix] = mirror
    return list(mirror_dict.values())

def generate_index_html(data):
    """
    生成主页HTML
    """
    last_updated = data.get("last_updated", "")
    try:
        last_time = datetime.fromisoformat(last_updated).strftime("%Y-%m-%d %H:%M:%S UTC")
    except:
        last_time = last_updated

    # 去重处理
    unique_mirrors = deduplicate_mirrors(data["mirrors"])

    available_mirrors = [m for m in unique_mirrors if m["available"]]
    unavailable_mirrors = [m for m in unique_mirrors if not m["available"]]
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="GitHub镜像加速地址列表 - 实时可用的GitHub镜像地址">
    <title>GitHub镜像加速地址列表</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .header {{
            background: white;
            border-radius: 16px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            color: #333;
            margin-bottom: 15px;
        }}
        
        .header .subtitle {{
            color: #666;
            font-size: 1.1em;
            margin-bottom: 20px;
        }}
        
        .stats {{
            display: flex;
            justify-content: center;
            gap: 40px;
            flex-wrap: wrap;
            margin-top: 20px;
        }}
        
        .stat-item {{
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .stat-label {{
            color: #666;
            margin-top: 5px;
        }}
        
        .last-updated {{
            margin-top: 20px;
            color: #999;
            font-size: 0.9em;
        }}
        
        .section {{
            background: white;
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        }}
        
        .section-title {{
            font-size: 1.5em;
            color: #333;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .mirror-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }}
        
        .mirror-card {{
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            padding: 20px;
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        
        .mirror-card:hover {{
            border-color: #667eea;
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.2);
        }}
        
        .mirror-card.available {{
            border-color: #4caf50;
            background: linear-gradient(135deg, #f8fff8 0%, #fff 100%);
        }}
        
        .mirror-card.unavailable {{
            border-color: #f44336;
            background: linear-gradient(135deg, #fff8f8 0%, #fff 100%);
            opacity: 0.6;
        }}
        
        .mirror-card-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 15px;
        }}
        
        .mirror-name {{
            font-size: 1.2em;
            font-weight: bold;
            color: #333;
        }}
        
        .status-badge {{
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
        }}
        
        .status-badge.available {{
            background: #4caf50;
            color: white;
        }}
        
        .status-badge.unavailable {{
            background: #f44336;
            color: white;
        }}
        
        .mirror-url {{
            background: #f5f5f5;
            padding: 10px;
            border-radius: 8px;
            font-family: "Courier New", monospace;
            font-size: 0.9em;
            word-break: break-all;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        
        .mirror-url span {{
            flex: 1;
            margin-right: 10px;
        }}
        
        .copy-btn {{
            background: #667eea;
            color: white;
            border: none;
            padding: 5px 15px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.85em;
            transition: background 0.3s;
            white-space: nowrap;
        }}
        
        .copy-btn:hover {{
            background: #5568d3;
        }}
        
        .mirror-info {{
            display: flex;
            gap: 20px;
            color: #666;
            font-size: 0.9em;
        }}
        
        .info-item {{
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        
        .info-label {{
            font-weight: 600;
        }}
        
        .usage {{
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 15px;
            margin-top: 30px;
            border-radius: 8px;
        }}
        
        .usage h3 {{
            color: #333;
            margin-bottom: 10px;
        }}
        
        .usage code {{
            background: #e0e0e0;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: "Courier New", monospace;
        }}
        
        .footer {{
            text-align: center;
            color: white;
            padding: 20px;
            margin-top: 30px;
        }}
        
        .footer a {{
            color: white;
            text-decoration: underline;
        }}
        
        @media (max-width: 768px) {{
            .header {{
                padding: 20px;
            }}
            
            .header h1 {{
                font-size: 1.8em;
            }}
            
            .stats {{
                gap: 20px;
            }}
            
            .mirror-grid {{
                grid-template-columns: 1fr;
            }}
            
            .mirror-info {{
                flex-direction: column;
                gap: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚡ GitHub镜像加速地址列表</h1>
            <p class="subtitle">实时检测的GitHub镜像加速服务</p>
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-value">{len(available_mirrors)}</div>
                    <div class="stat-label">可用镜像</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{len(data['mirrors'])}</div>
                    <div class="stat-label">总计检测</div>
                </div>
            </div>
            <p class="last-updated">🕐 最后更新: {last_time}</p>
        </div>
        
        <div class="section">
            <div class="section-title">✅ 可用镜像</div>
            <div class="mirror-grid">
"""
    
    for mirror in available_mirrors:
        response_time = mirror.get("response_time", "N/A")
        html += f"""
                <div class="mirror-card available">
                    <div class="mirror-card-header">
                        <div class="mirror-name">{mirror['name']}</div>
                        <span class="status-badge available">可用</span>
                    </div>
                    <div class="mirror-url">
                        <span id="url-{hash(mirror['prefix'])}">{mirror['prefix']}</span>
                        <button class="copy-btn" onclick="copyToClipboard('{mirror['prefix']}')">复制</button>
                    </div>
                    <div class="mirror-info">
                        <div class="info-item">
                            <span class="info-label">响应时间:</span> {response_time}ms
                        </div>
                    </div>
                </div>
"""
    
    html += """
            </div>
        </div>
"""
    
    if unavailable_mirrors:
        html += """
        <div class="section">
            <div class="section-title">❌ 不可用镜像</div>
            <div class="mirror-grid">
"""
        
        for mirror in unavailable_mirrors:
            message = mirror.get("message", "未知原因")
            html += f"""
                <div class="mirror-card unavailable">
                    <div class="mirror-card-header">
                        <div class="mirror-name">{mirror['name']}</div>
                        <span class="status-badge unavailable">不可用</span>
                    </div>
                    <div class="mirror-info">
                        <div class="info-item">
                            <span class="info-label">原因:</span> {message}
                        </div>
                    </div>
                </div>
"""
        
        html += """
            </div>
        </div>
"""
    
    html += f"""
        <div class="section">
            <div class="section-title">📖 使用说明</div>
            <div class="usage">
                <h3>Git Clone 使用方法</h3>
                <p>将镜像前缀添加到原始GitHub地址前面：</p>
                <br>
                <p>原始地址：</p>
                <code>git clone https://github.com/user/repo.git</code>
                <br><br>
                <p>使用镜像：</p>
                <code>git clone <镜像前缀>user/repo.git</code>
                <br><br>
                <p>例如：</p>
                <code>git clone https://mirror.ghproxy.com/user/repo.git</code>
            </div>
        </div>
        
        <div class="footer">
            <p>数据由GitHub Actions自动更新 • <a href="https://github.com">GitHub</a></p>
        </div>
    </div>
    
    <script>
        function copyToClipboard(text) {{
            navigator.clipboard.writeText(text).then(function() {{
                alert('已复制: ' + text);
            }}, function(err) {{
                prompt('复制失败，请手动复制:', text);
            }});
        }}
    </script>
</body>
</html>
"""
    
    return html

def save_html(html, filename="docs/index.html"):
    """
    保存HTML文件
    """
    # 确保使用项目根目录的完整路径
    if not os.path.isabs(filename):
        filename = os.path.join(PROJECT_ROOT, filename)
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"HTML页面已生成: {filename}")

def main():
    """
    主函数
    """
    print("=" * 60)
    print("GitHub Pages页面生成工具")
    print("=" * 60)

    # 加载镜像数据
    mirrors_data = load_mirrors()

    # 显示去重前的数量
    original_count = len(mirrors_data["mirrors"])
    print(f"原始镜像数量: {original_count}")

    # 生成HTML
    html = generate_index_html(mirrors_data)

    # 保存HTML
    save_html(html)

    # 更新总数统计
    unique_mirrors = deduplicate_mirrors(mirrors_data["mirrors"])
    print(f"去重后镜像数量: {len(unique_mirrors)}")
    print(f"去重数量: {original_count - len(unique_mirrors)}")

    print("=" * 60)
    print("完成!")

if __name__ == "__main__":
    main()
