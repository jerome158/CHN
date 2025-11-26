from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import os

def download_m3u_content():
    print("开始下载M3U文件内容...")
    
    # 配置Chrome选项
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    
    try:
        # 使用WebDriver Manager自动管理驱动
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        url = 'https://bc.188766.xyz/?ip=&mishitong=true&mima=mianfeibuhuaqian&json=true'
        print(f'正在访问: {url}')
        
        driver.get(url)
        time.sleep(15)
        
        content = driver.page_source
        print('页面加载完成')
        
        with open('mig2.txt', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print('内容已保存到 mig2.txt')
        
    except Exception as e:
        print(f'错误: {e}')
        
    finally:
        if 'driver' in locals():
            driver.quit()
            print('浏览器已关闭')

if __name__ == "__main__":
    download_m3u_content()
