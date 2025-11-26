M3UDownloader:
    def __init__(self):
        self.setup_browser()
        
    def setup_browser(self):
        """配置浏览器选项"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        
    def download_with_selenium(self, url):
        """使用Selenium绕过Cloudflare防护"""
        print("启动Chrome浏览器...")
        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            print(f"正在访问: {url}")
            driver.get(url)
            
            # 智能等待策略
            wait = WebDriverWait(driver, 45)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            # 检查Cloudflare挑战
            page_source = driver.page_source
            if self.is_cloudflare_challenge(page_source):
                print("检测到Cloudflare防护，执行智能等待...")
                return self.handle_cloudflare_challenge(driver, url)
                
        except Exception as e:
            print(f"Selenium下载失败: {str(e)}")
            return None
            
        finally:
            driver.quit()
            
    def is_cloudflare_challenge(self, page_source):
        """检测是否为Cloudflare挑战页面"""
        cloudflare_indicators = [
            "Just a moment",
            "Cloudflare",
            "challenge"
        ]
        return any(indicator in page_source for indicator in cloudflare_indicators)
        
    def handle_cloudflare_challenge(self, driver, url):
        """处理Cloudflare挑战"""
        max_wait_time = 60
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            current_source = driver.page_source
            if not self.is_cloudflare_challenge(current_source):
                print("Cloudflare挑战完成，获取内容...")
                return current_source
                
            time.sleep(2)
            
        print("Cloudflare挑战超时")
        return None
        
    def save_content(self, content, filename="mig2.txt"):
        """保存内容到文件"""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
                
            file_size = os.path.getsize(filename)
            print(f"内容已保存到 {filename}")
            print(f"文件大小: {file_size} 字节")
            return True
            
        except Exception as e:
            print(f"保存文件失败: {str(e)}")
            return False

if __name__ == "__main__":
    downloader = M3UDownloader()
    target_url = "https://bc.188766.xyz/?ip=&mishitong=true&mima=mianfeibuhuaqian&json=true"
    
    print("开始下载M3U文件内容...")
    
    # 尝试多种下载方法
    content = downloader.download_with_selenium(target_url)
    
    if content:
        downloader.save_content(content)
    else:
        print("下载失败")


