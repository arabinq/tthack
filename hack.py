from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import random
import time
from threading import Thread


class Tthack:
    def __init__(self, school, username, password, type):
        self.school = school
        self.username = username
        self.password = password
        self.type = type
        self.login_school = driver.find_element_by_xpath('//*[@id="mat-input-0"]')
        self.login_school.send_keys(self.school)
        time.sleep(0.5)
        self.login_school.send_keys(Keys.RETURN)
        time.sleep(0.5)
        self.login_username = driver.find_element_by_xpath('//*[@id="mat-input-1"]')
        self.login_username.send_keys(self.username)
        driver.find_element_by_xpath('/html/body/ttr-root/ttr-root-app/div/div/section/ttr-login2/ttr-splash/div/div/div/ttr-login-form/div/form/mat-card/div[3]/div[2]/button').click()
        self.login_password = driver.find_element_by_xpath('//*[@id="mat-input-2"]')
        self.login_password.send_keys(self.password, Keys.RETURN)
        time.sleep(2)
        driver.get('https://play.ttrockstars.com/play?mode=' + self.type)
        time.sleep(5)

    def launch(self):
        if self.type == 'garage':
            self.question_xpath = '/html/body/ttr-root/ttr-root-app/div/div/section/ttr-garage/ttr-game-holder/div/div/div/ttr-game-footpedal/section[2]/section/section/ttr-game-question/span[2]'
            self.play = driver.find_element_by_xpath('/html/body/ttr-root/ttr-root-app/div/div/section/ttr-play-page/section/div/ttr-garage-preview/ttr-game-preview/mat-card/div[1]/div[1]/section/section')
            self.play.click()
        elif self.type == 'festival':
            self.question_xpath = '/html/body/ttr-root/ttr-root-app/div/div/section/ttr-festival/ttr-game-holder/div/div/div/ttr-game-footpedal/section[2]/section/section/ttr-game-question/span[2]'
            self.play = driver.find_element_by_xpath('/html/body/ttr-root/ttr-root-app/div/div/section/ttr-play-page/section/div/ttr-festival-preview/ttr-game-preview/mat-card/div[2]/ttr-game-stages/div/div[1]/ttr-game-stage/button')
            self.play.click()
            self.timer = int(driver.find_element_by_xpath('/html/body/ttr-root/ttr-root-app/div/div/section/ttr-play-page/section/div/ttr-festival-preview/ttr-game-preview/mat-card/div[2]/ttr-game-stages/div/div[1]/ttr-game-stage/div').text.strip())
            time.sleep(self.timer)
        while True:
            time.sleep(5)
            self.t_end = time.time() + 60 * 3
            while time.time() < self.t_end:
                time.sleep(0.2)
                try:
                    self.answer = self.parse_question(driver.find_element_by_xpath(self.question_xpath))
                    driver.find_element_by_xpath('/html/body').send_keys(self.answer, Keys.ENTER)
                except:
                    break
            time.sleep(6)
            self.play_again = driver.find_element_by_xpath('/html/body/ttr-root/ttr-root-app/div/div/section/ttr-garage/ttr-game-holder/div/div/div/button[2]')
            self.play_again.click()

    def parse_question(self, location):
        self.location = location
        self.text = self.location.text
        self.word_list = self.text.split()
        if '÷' in self.text:
            self.ans = int(int(self.word_list[0]) / int(self.word_list[2]))
        elif '×' in self.text:
            self.ans = int(int(self.word_list[0]) * int(self.word_list[2]))
        return str(self.ans)





if __name__ == '__main__':
    path = 'D:\coding\chromedriver.exe'
    driver = webdriver.Chrome(path)
    driver.get('https://play.ttrockstars.com/auth/school/student')
    time.sleep(2)
    hack = Tthack('al-fu', 'hassha', 'yyk', 'festival')
    hack.launch()
