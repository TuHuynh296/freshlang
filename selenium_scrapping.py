import time
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.chrome.options import Options
import re
from PyQt5 import QtCore

class Scraping():
    def __init__(self, index_get):
        chrome_path = 'D:/Soft/chromedriver_win32/chromedriver.exe'
        # keep selenium always open until ended code
        # opts = ChromeOptions()
        # opts.add_experimental_option("detach", True)
        #self.driver = Chrome(executable_path = chrome_path, chrome_options= opts) 
        options = Options()
        options.add_argument("--use-fake-ui-for-media-stream")
        #options.add_argument('--headless')
        self.driver = Chrome(executable_path = chrome_path, chrome_options= options)
        if index_get == 0:
            self.driver.get('https://translate.google.com/#view=home&op=translate&sl=en&tl=vi&text=')

    def google_translate(self, sentence, mode):
        mode = 'en&tl=vi' if mode == 'e2v' else 'vi&tl=en'
        self.driver.get('https://translate.google.com/#view=home&op=translate&sl=%s&text=%s'%(mode, sentence))
        time.sleep(0.5)
        translated = ''
        spelling = None
        word_type = None
        hint = None
        contents_of_word_type = None
        try:
            spelling = self.driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div/div/div[3]/div[1]').text
            word_type = self.driver.find_elements_by_class_name('gt-baf-pos-head')
            word_type = [x.text.replace('\nFrequency', '') for x in word_type]
            contents_of_word_type = self.driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[2]/div[3]/div[2]/div[1]/div[1]/div').text.split('\n')
            del(contents_of_word_type[0])
            del(contents_of_word_type[1])
        except:
            pass

        try:
            hint = self.driver.find_element_by_class_name('gt-related-suggest-message').text.split('\n')
        except:
            try:
                hint = self.driver.find_element_by_class_name('gt-spell-correct-message').text.split('\n')
            except:
                pass
        translated = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div[1]/div[2]/div/span[1]').text

        display_wordtype = self.driver.find_element_by_class_name('gt-cd-baf').get_attribute('style')
        display_hint = self.driver.find_element_by_id('spelling-correction').get_attribute('style')
        if display_wordtype == 'display: none;':
            word_type = None
        if display_hint == 'display: none;':
            hint = None
        return [translated, spelling, (word_type, contents_of_word_type), hint]

    def speech_to_text(self, ui):
        speech_button = wait(self.driver, timeout = 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gt-speech"]/span')))
        def status_s2t():
            status = self.driver.find_element_by_xpath('//*[@id="gt-speech"]')
            return status.get_attribute('data-tooltip').split(' ')[1]
        # remove_input = self.driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div')
        # remove_input.click()
        if status_s2t() == 'on':
            speech_button.click()
        ui.st2_waiting = True
        time_waiting = len(ui.parent.GetLang('ENG').split(' '))*1000
        time_waiting = 3000 if time_waiting <= 2000 else int(time_waiting*0.8)
        def waiting(speech_button):
            result = self.driver.find_element_by_xpath('//*[@id="input-wrap"]/div[2]').get_attribute('textContent')
            ui.lineEdit.setReadOnly(False)
            ui.lineEdit.setText(result)
            ui.lineEdit.setReadOnly(True)
            ui.st2_waiting = False
            ui.lineEdit.setPlaceholderText('Listening stopped !')
            if status_s2t() == 'off':
                speech_button.click()
        QtCore.QTimer.singleShot(time_waiting, lambda: waiting(speech_button))
        
