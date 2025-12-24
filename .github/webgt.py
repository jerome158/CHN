
import requests
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import re

def clean_url(url, base_url):
    """清理和规范化URL"""
    url = url.strip()
    if not url:
        return None
    
    # 移除常见的HTML实体和多余字符
    url = url.replace('&amp;', '&').replace('"', '').replace("'", '')
    
    # 检查是否为有效协议开头
    valid_schemes = ('http://', 'https://', 'rtmp://', 'rtsp://', 'mms://', 'udp://')
    if any(url.startswith(scheme) for scheme in valid_schemes):
        return url
    
    # 处理相对URL
    if url.startswith('/') or url.startswith('./') or url.startswith('../'):
        try:
            return urljoin(base_url, url)
        except:
            pass
            
    return None

def extract_urls_from_cell(cell, base_url):
    """从表格单元格中提取所有有效URL"""
    urls = []
    
    # 方法1: 查找所有<a>标签的href属性
    for link in cell.find_all('a', href=True):
        href = clean_url(link['href'], base_url)
        if href:
            urls.append(href)
    
    # 方法2: 查找script标签中的URL
    for script in cell.find_all('script'):
        if script.string:
            # 使用正则表达式查找各种协议的URL
            url_patterns = re.findall(
                r'(?:https?|rtmp|rtsp|mms|udp)://[^\s"\';<>\)]+', 
                script.string
            )
            for pattern_url in url_patterns:
                cleaned = clean_url(pattern_url, base_url)
                if cleaned:
                    urls.append(cleaned)
    
    # 方法3: 直接从文本内容中提取URL
    raw_text = cell.get_text(separator=' ', strip=True)
    # 分割文本并检查每部分是否为URL
    for part in re.split(r'\s+', raw_text):
        cleaned = clean_url(part, base_url)
        if cleaned:
            urls.append(cleaned)
    
    # 去重并返回
    return list(set(urls))

def main():
    target_url = 'https://www.wmviv.com/bingchatv.html'
    output_file = 'live_channels.txt'
    
    print(f"开始抓取直播频道列表: {target_url}")
    
    try:
        # 设置请求头模拟浏览器访问
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # 发送HTTP GET请求
        response = requests.get(target_url, headers=headers, timeout=30)
        response.raise_for_status()
        
    except requests.RequestException as e:
        print(f"错误: 无法访问目标网页 {target_url}")
        print(f"详细信息: {e}")
        sys.exit(1)
    
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 查找包含"冰茶TV直播列表"的表格
    tables = soup.find_all('table')
    target_table = None
    
    # 策略1: 查找包含特定文本的表格
    for table in tables:
        if table.find(string=re.compile("冰茶TV直播列表")):
            target_table = table
            break
    
    # 策略2: 查找包含关键列名的表格
    if not target_table:
        for table in tables:
            if (table.find(string="频道名称") and 
                (table.find(string="播放地址") or table.find(string="调用地址"))):
                target_table = table
                break
    
    # 策略3: 使用第一个较大的表格
    if not target_table and tables:
        target_table = max(tables, key=lambda t: len(t.find_all('tr')))
    
    if not target_table:
        print("错误: 未在页面中找到包含频道数据的表格")
        sys.exit(1)
    
    print("成功定位到直播列表表格")
    
    # 获取表头以确定列索引
    rows = target_table.find_all('tr')
    if not rows:
        print("错误: 表格中没有找到数据行")
        sys.exit(1)
    
    # 确定关键列的索引
    header_row = rows[0]
    headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]
    
    # 初始化列索引映射
    column_indices = {
        'channel_name': None,
        'play_url': None,
        'call_url': None
    }
    
    # 自动识别列索引
    for i, header in enumerate(headers):
        if "频道名称" in header:
            column_indices['channel_name'] = i
        elif "播放地址" in header:
            column_indices['play_url'] = i
        elif "调用地址" in header:
            column_indices['call_url'] = i
    
    # 如果自动识别失败，使用默认索引(基于常见表格结构)
    if column_indices['channel_name'] is None:
        column_indices['channel_name'] = 2  # 通常第3列为频道名称
    if column_indices['play_url'] is None:
        column_indices['play_url'] = 3      # 通常第4列为播放地址
    if column_indices['call_url'] is None:
        column_indices['call_url'] = 4      # 通常第5列为调用地址
    
    print(f"列索引映射: 频道名称={column_indices['channel_name']}, "
          f"播放地址={column_indices['play_url']}, "
          f"调用地址={column_indices['call_url']}")
    
    # 存储格式化后的频道数据
    output_lines = []
    
    # 遍历数据行(跳过表头)
    for row in rows[1:]:
        cells = row.find_all(['td', 'th'])
        
        # 确保行有足够的列数
        if len(cells) <= max(idx for idx in column_indices.values() if idx is not None):
            continue
        
        # 提取频道名称
        channel_name_cell = cells[column_indices['channel_name']]
        channel_name = channel_name_cell.get_text(strip=True)
        
        # 跳过空行或无效频道
        if not channel_name:
            continue
        
        # 提取播放地址和调用地址
        all_urls = []
        
        # 处理播放地址列
        if column_indices['play_url'] is not None:
            play_url_cell = cells[column_indices['play_url']]
            play_urls = extract_urls_from_cell(play_url_cell, target_url)
            all_urls.extend(play_urls)
        
        # 处理调用地址列
        if column_indices['call_url'] is not None:
            call_url_cell = cells[column_indices['call_url']]
            call_urls = extract_urls_from_cell(call_url_cell, target_url)
            all_urls.extend(call_urls)
        
        # 为每个URL生成独立的输出行
        for url in all_urls:
            if url:  # 确保URL有效
                output_lines.append(f"{channel_name},{url}")
    
    # 去重并排序
    unique_lines = sorted(list(set(output_lines)))
    
    # 写入输出文件
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(unique_lines))
    except IOError as e:
        print(f"错误: 无法写入文件 {output_file}")
        print(f"详细信息: {e}")
        sys.exit(1)
    
    print(f"成功生成频道列表文件!")
    print(f"总共提取了 {len(unique_lines)} 条频道地址")
    print(f"数据已保存至: {output_file}")
    
    # 显示前几行作为示例
    if unique_lines:
        print("\n前5行示例数据:")
        for i, line in enumerate(unique_lines[:5]):
            print(f"  {i+1}. {line}")

if __name__ == "__main__":
    main()
