import requests
import os
import time
from pathlib import Path

def download_m3u_file():
    """
    下载M3U文件的函数，使用requests库直接获取内容
    """
    url = "https://bc.188766.xyz/?ip=&mishitong=true&mima=mianfeibuhuaqian&json=true"
    
    # 设置浏览器User-Agent，模拟真实浏览器请求
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Referer': 'https://bc.188766.xyz/'
    }
    
    try:
        print(f"正在下载M3U文件: {url}")
        
        # 发送GET请求
        response = requests.get(url, headers=headers, timeout=30)
        
        # 检查响应状态
        if response.status_code == 200:
            content = response.text
            file_size = len(content)
            print(f"下载成功，文件大小: {file_size} 字节")
            
            # 验证内容是否为有效的M3U文件
            if content.strip().startswith('#EXTM3U'):
                # 保存文件
                output_file = 'playlist.m3u'
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"文件已保存为: {output_file}")
                
                # 检查文件是否发生变化
                old_content = ""
                if os.path.exists(output_file + '.old'):
                    with open(output_file + '.old', 'r', encoding='utf-8') as f:
                        old_content = f.read()
                
                # 如果内容发生变化，设置输出变量
                if content != old_content:
                    # 保存旧内容用于下次比较
                    with open(output_file + '.old', 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print("::set-output name=changed::true")
                return True
            else:
                print(f"错误：下载的内容不是有效的M3U文件")
                print(f"内容开头: {content[:100]}...")
                return False
        else:
            print(f"错误：HTTP状态码 {response.status_code}")
            print(f"响应头: {response.headers}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"网络请求错误: {e}")
        return False
    except Exception as e:
        print(f"未知错误: {e}")
        return False

if __name__ == "__main__":
    download_m3u_file()

