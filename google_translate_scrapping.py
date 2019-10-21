import time
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.chrome.options import Options

class GoogleTrans():
    def __init__(self):
        chrome_path = 'D:/Soft/chromedriver_win32/chromedriver.exe'
        # keep selenium always open until ended code
        # opts = ChromeOptions()
        # opts.add_experimental_option("detach", True)
        #self.driver = Chrome(executable_path = chrome_path, chrome_options= opts) 
        options = Options()
        options.add_argument("--use-fake-ui-for-media-stream")
        options.add_argument('--headless')
        self.driver = Chrome(executable_path = chrome_path, chrome_options= options)

    def translate(self, sentence):
        self.driver.get('https://translate.google.com/#view=home&op=translate&sl=en&tl=vi&text=%s'%(sentence))
        time.sleep(0.5)
        translated = wait(self.driver, timeout = 10).until(
            EC.presence_of_element_located(
                (By.XPATH, 
                '/html/body/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div[1]/div[2]/div/span[1]'))).text
        return translated

    def speech_to_text(self):
        speech_button = wait(self.driver, timeout = 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gt-speech"]/span')))
        status = self.driver.find_element_by_xpath('//*[@id="gt-speech"]')
        status = status.get_attribute('data-tooltip').split(' ')[1]
        remove_input = self.driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div')
        remove_input.click()
        if status == 'on':
            speech_button.click()
        time.sleep(10)
        result = self.driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div[1]/div[2]/div/span[1]/span')
        print(result.text)
        speech_button.click()


