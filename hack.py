from selenium import webdriver
from selenium.webdriver.common.by import By
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

    def launch(self):
        pass




if __name__ == '__main__':
    path = 'D:\coding\chromedriver.exe'
    driver = webdriver.Chrome(path)
    driver.get('https://play.ttrockstars.com/auth/school/student')
    time.sleep(2)
    hack = Tthack('al-fu', 'hassha', 'yyk')
    hack.launch()
