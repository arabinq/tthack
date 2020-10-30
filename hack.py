from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

class Tthack:
    def __init__(self, school, username, password):
        self.school = school
        self.username = username
        self.password = password
        self.login_school = driver.find_element_by_xpath('//*[@id="mat-input-0"]')
        self.login_school.send_keys(self.school)
        time.sleep(0.5)
        self.login_school.send_keys(Keys.ENTER)
        time.sleep(0.5)
        driver.find_element_by_xpath('//*[@id="mat-input-1"]').send_keys(self.username)
        driver.find_element_by_xpath('/html/body/ttr-root/ttr-root-app/div/div/section/ttr-login2/ttr-splash/div/div/div/ttr-login-form/div/form/mat-card/div[3]/div[2]/button').click()
        driver.find_element_by_xpath('//*[@id="mat-input-2"]').send_keys(self.password, Keys.RETURN)
        time.sleep(2)

    def launch(self):
        self.play = driver.find_element_by_xpath('/html/body/ttr-root/ttr-root-app/div/div/section/ttr-play-page/section/div/ttr-garage-preview/ttr-game-preview/mat-card/div[1]/div[1]/section/section')
        self.play.click()
        time.sleep(7)
        self.question_xpath = '/html/body/ttr-root/ttr-root-app/div/div/section/ttr-garage/ttr-game-holder/div/div/div/ttr-game-footpedal/section[2]/section/section/ttr-game-question/span[2]'
        while True:
            self.answer = self.parse_question(driver.find_element_by_xpath(self.question_xpath))
            driver.find_element_by_xpath('/html/body').send_keys(self.answer, Keys.ENTER)
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.text_to_be_present_in_element((By.CLASS_NAME, "stamp center mat-white-color"), "Game Over!!")
                )
                print('game ended')
            except:
                print('game in progress')

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
    hack = Tthack('al-fu', 'hassha', 'yyk')
    hack.launch()
