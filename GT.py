from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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
    
    # 关键修正：指定正确的Chromium浏览器路径
    options.binary_location = '/usr/bin/chromium-browser'
    
    try:
        # 初始化浏览器驱动
        print("启动Chrome浏览器...")
        driver = webdriver.Chrome(options=options)
        
        # 目标URL
        url = 'https://bc.188766.xyz/?ip=&mishitong=true&mima=mianfeibuhuaqian&json=true'
        print(f'正在访问: {url}')
        
        # 访问页面
        driver.get(url)
        
        # 等待页面加载
        print('等待页面加载...')
        time.sleep(30)
        
        # 获取页面内容
        content = driver.page_source
        print('页面加载完成')
        
        # 保存到文件
        with open('mig2.txt', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print('内容已保存到 mig2.txt')
        
        # 验证文件
        if os.path.exists('mig2.txt'):
            file_size = os.path.getsize('mig2.txt')
            print(f'文件大小: {file_size} 字节')
            
    except Exception as e:
        print(f'错误: {e}')
        
    finally:
        if 'driver' in locals():
            driver.quit()
            print('浏览器已关闭')

if __name__ == "__main__":
    download_m3u_content()

