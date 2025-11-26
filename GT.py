from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os

def download_m3u_content():
    print("开始下载M3U文件内容...")
    
    # 配置Chrome选项
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    
    try:
        # 初始化浏览器驱动
        print("启动Chrome浏览器...")
        driver = webdriver.Chrome(options=options)
        
        # 目标URL
        url = 'https://bc.188766.xyz/?ip=&mishitong=true&mima=mianfeibuhuaqian&json=true'
        print(f'正在访问: {url}')
        
        # 访问页面
        driver.get(url)
        
        # 等待页面加载和CloudFlare挑战完成
        print('等待页面加载...')
        time.sleep(15)
        
        # 获取页面内容
        content = driver.page_source
        print('页面加载完成')
        
        # 检查是否成功绕过CloudFlare
        if "Just a moment" in content or "CloudFlare" in content:
            print("警告：可能仍在CloudFlare挑战页面")
        else:
            print("成功获取页面内容")
        
        # 保存到文件
        with open('mig2.txt', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print('内容已保存到 mig2.txt')
        
        # 检查文件内容
        file_size = os.path.getsize('mig2.txt')
        print(f'文件大小: {file_size} 字节')
        
        # 显示前几行内容预览
        with open('mig2.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f'文件包含 {len(lines)} 行内容')
        if lines:
            print("前3行内容预览:")
            for i, line in enumerate(lines[:3]):
                print(f"第{i+1}行: {line.strip()}")
            
    except Exception as e:
        print(f'错误: {e}')
        
    finally:
        # 确保浏览器关闭
        if 'driver' in locals():
            driver.quit()
            print('浏览器已关闭')

if __name__ == "__main__":
    download_m3u_content()
