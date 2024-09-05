import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys    
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

class Chat:
    
    def __init__(self, chat):
        self.chat = chat
    
    def prompt(self, prompt, profile, num, head):
        try:
            subprocess.call("TASKKILL /f  /IM  CHROME.EXE")
            subprocess.call("TASKKILL /f  /IM  CHROMEDRIVER.EXE")
        except:
            pass

        options = uc.ChromeOptions() 
        if head == True:
            options.add_argument('-headless')
        options.add_argument(r'--user-data-dir=' + profile + '')
        options.add_argument(r'--profile-directory=Profile ' + num + '')
        driver = uc.Chrome(options=options)
        driver.maximize_window()
        driver.execute_script(f"location.href='https://chatgpt.com';")
        driver.switch_to.window(driver.window_handles[0])
        
        text = ""
        l = 0
        
        while text == "" and l < 10:
            
            try:#Prompt Area 
                driver.find_element(By.CSS_SELECTOR, "#prompt-textarea").clear()
                driver.find_element(By.CSS_SELECTOR, "#prompt-textarea").send_keys(prompt)
            except:
                pass
            
            try: #Enter
                driver.find_element(By.CSS_SELECTOR, "#prompt-textarea").send_keys(Keys.RETURN);
            except:
                pass

            time.sleep(10)
            
            try: #Get Response
                text = driver.find_element(By.CSS_SELECTOR, ".markdown > p:nth-child(1)").text
            except:
                pass
            
            l += 1
        
        driver.quit()
        
        try:
            subprocess.call("TASKKILL /f  /IM  CHROME.EXE")
            subprocess.call("TASKKILL /f  /IM  CHROMEDRIVER.EXE")
        except:
            pass
        
        return text