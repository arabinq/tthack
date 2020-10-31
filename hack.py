import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import time
import sys
import os
import math

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

class Bot:
    def __init__(self):
        self.path = resource_path('./driver/chromedriver.exe')


    def login(self, school, username, password, type, rounds):
        global gui
        global driver

        self.school = school
        self.username = username
        self.password = password
        self.rounds = rounds
        self.type = type
        self.coins = 0

        gui.update_status('Logging in...')
        driver = webdriver.Chrome(self.path)
        gui.update_status('Inputting school...')
        driver.get('https://play.ttrockstars.com/auth/school/student')
        try:
            self.login_school = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="mat-input-0"]'))
            )
        except:
            driver.quit()
            gui.update_status('Error: Problem Loading Page.')
            return None
        self.login_school.send_keys(self.school)
        time.sleep(1)
        self.login_school.send_keys(Keys.RETURN)
        try:
            self.login_username = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="mat-input-1"]'))
            )
            gui.update_status('Inputting Username...')
        except:
            driver.quit()
            gui.update_status('Error: Invalid School')
            return None
        self.login_username.send_keys(self.username)
        driver.find_element_by_xpath('/html/body/ttr-root/ttr-root-app/div/div/section/ttr-login2/ttr-splash/div/div/div/ttr-login-form/div/form/mat-card/div[3]/div[2]/button').click()
        gui.update_status('Inputting Password...')
        try:
            self.login_password = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="mat-input-2"]'))
            )
        except:
            driver.quit()
            gui.update_status('Error: Problem Loading Page.')
            return None
        self.login_password.send_keys(self.password, Keys.RETURN)
        time.sleep(2)
        try:
            self.error = driver.find_element_by_xpath('/html/body/ttr-root/ttr-root-app/div/div/section/ttr-login2/ttr-splash/div/div/div/ttr-login-form/div/form/mat-card/div[2]/h2')
            driver.quit()
            gui.update_status('Error: Incorrect Login Details')
            return None
        except:
            gui.update_status('Login Successful...')
        driver.get('https://play.ttrockstars.com/play?mode=' + self.type)
        time.sleep(3)
        self.launch()

    def launch(self):
        global driver
        global gui


        gui.update_status(f'Going Into {self.type} Game...')
        self.game_info = self.get_type_info()
        if self.type != 'festival':
            self.play.click()
        for i in range(0, int(self.rounds)):
            gui.update_status('answering questions...')
            time.sleep(6)
            self.t_end = time.time() + 60 * 3
            while time.time() < self.t_end:
                try:
                    self.find_question = WebDriverWait(driver, 1, poll_frequency=0.2).until(
                        EC.presence_of_element_located((By.XPATH, self.game_info[0]))
                    )
                    self.answer = self.parse_question(driver.find_element_by_xpath(self.game_info[0]))
                    driver.find_element_by_xpath('/html/body').send_keys(self.answer, Keys.ENTER)
                except:
                    break
            gui.update_status('game ended, going into new game...')
            time.sleep(6)
            self.coins += self.get_coins(driver.find_element_by_xpath(self.game_info[2]))
            gui.update_coins(str(self.coins))
            self.play_again = driver.find_element_by_xpath(self.game_info[1])
            self.play_again.click()

        gui.update_status('Hack ended')

    def get_coins(self, location):
        self.location = location
        self.new_coins = int(self.location.text)
        return self.new_coins

    def parse_question(self, location):
        self.location = location
        self.text = self.location.text
        self.word_list = self.text.split()
        if '÷' in self.text:
            self.ans = int(int(self.word_list[0]) / int(self.word_list[2]))
        elif '×' in self.text:
            self.ans = int(int(self.word_list[0]) * int(self.word_list[2]))
        return str(self.ans)

    def get_type_info(self):
        if self.type == 'garage':
            self.question_xpath = '/html/body/ttr-root/ttr-root-app/div/div/section/ttr-garage/ttr-game-holder/div/div/div/ttr-game-footpedal/section[2]/section/section/ttr-game-question/span[2]'
            self.play_again_xpath = '/html/body/ttr-root/ttr-root-app/div/div/section/ttr-garage/ttr-game-holder/div/div/div/button[2]'
            self.play = driver.find_element_by_xpath('/html/body/ttr-root/ttr-root-app/div/div/section/ttr-play-page/section/div/ttr-garage-preview/ttr-game-preview/mat-card/div[1]/div[1]/section/section')
        elif self.type == 'festival':
            self.question_xpath = '/html/body/ttr-root/ttr-root-app/div/div/section/ttr-festival/ttr-game-holder/div/div/div/ttr-game-footpedal/section[2]/section/section/ttr-game-question/span[2]'
            self.play_again_xpath = '/html/body/ttr-root/ttr-root-app/div/div/section/ttr-garage/ttr-game-holder/div/div/div/button[2]'
            self.play = driver.find_element_by_xpath('/html/body/ttr-root/ttr-root-app/div/div/section/ttr-play-page/section/div/ttr-festival-preview/ttr-game-preview/mat-card/div[2]/ttr-game-stages/div/div[1]/ttr-game-stage/button')
            self.play.click()
            self.timer = int(driver.find_element_by_xpath('/html/body/ttr-root/ttr-root-app/div/div/section/ttr-play-page/section/div/ttr-festival-preview/ttr-game-preview/mat-card/div[2]/ttr-game-stages/div/div[1]/ttr-game-stage/div').text.strip())
            time.sleep(self.timer)
        elif self.type == 'studio':
            self.question_xpath = '/html/body/ttr-root/ttr-root-app/div/div/section/ttr-studio/ttr-game-holder/div/div/div/ttr-game-footpedal/section[2]/section/section/ttr-game-question/span[2]'
            self.play_again_xpath = '/html/body/ttr-root/ttr-root-app/div/div/section/ttr-studio/ttr-game-holder/div/div/div/button[2]'
            self.play = driver.find_element_by_xpath('/html/body/ttr-root/ttr-root-app/div/div/section/ttr-play-page/section/div/ttr-studio-preview/ttr-game-preview/mat-card/div[1]/div[1]/section/button')

        return self.question_xpath, self.play_again_xpath, '/html/body/ttr-root/ttr-root-app/div/div/section/ttr-garage/ttr-game-holder/div/div/ttr-game-results/div/div[2]/ttr-game-results-summary/div/div[1]/span[1]'

    def end(self):
        global driver
        driver.quit()
        gui.update_status('Ended Hack.')
        return None


class Gui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('TThack')
        self.geometry('200x440')

        self.type = tk.StringVar()
        self.status_message = tk.StringVar()
        self.coins_message = tk.StringVar()
        self.school_label = tk.Label(text="School", justify="left")
        self.school_entry = tk.Entry()
        self.username_label = tk.Label(text="Username")
        self.username_entry = tk.Entry()
        self.password_label = tk.Label(text="Password")
        self.password_entry = tk.Entry()
        self.rounds_label = tk.Label(text="Number Of Rounds")
        self.rounds_entry = tk.Entry()
        self.type_label = tk.Label(text="Game Mode")
        self.name_entry = tk.Entry(self)
        self.type_entry_one = tk.Radiobutton(text="Garage", value="garage", variable=self.type, command=self.disable_entry)
        self.type_entry_two = tk.Radiobutton(text="Festival", value="festival", variable=self.type, command=self.disable_entry)
        self.type_entry_three = tk.Radiobutton(text="Studio", value="studio", variable=self.type, command=self.disable_entry)
        self.type_entry_five = tk.Radiobutton(text="Soundcheck", value="soundcheck", variable=self.type, command=self.disable_entry)
        self.type_entry_six = tk.Radiobutton(text="Arena", value="arena", variable=self.type, command=self.disable_entry)
        self.type_entry_four = tk.Radiobutton(text="Rockslam", value="rockslam", variable=self.type, command=self.enable_entry)
        self.type.set('garage')
        self.submit = tk.Button(text="Start Hack", command=self.send_values)
        self.end = tk.Button(text="End Hack", command=bot.end)
        self.coins = tk.Label(textvariable=self.coins_message)
        self.coins_message.set('Coins Earned So Far: 0')
        self.status = tk.Label(textvariable=self.status_message)
        self.status_message.set('Waiting...')
        self.school_label.pack(anchor="w")
        self.school_entry.pack(anchor="w")
        self.username_label.pack(anchor="w")
        self.username_entry.pack(anchor="w")
        self.password_label.pack(anchor="w")
        self.password_entry.pack(anchor="w")
        self.rounds_label.pack(anchor="w")
        self.rounds_entry.pack(anchor="w")
        self.type_label.pack(anchor="w")
        self.type_entry_one.pack(anchor="w")
        self.type_entry_two.pack(anchor="w")
        self.type_entry_three.pack(anchor="w")
        self.type_entry_five.pack(anchor="w")
        self.type_entry_six.pack(anchor="w")
        self.type_entry_four.pack(anchor="w")
        self.submit.pack(anchor="w")
        self.end.pack(anchor="w")
        self.coins.pack(anchor="w")
        self.status.pack(anchor="w")

    def send_values(self):
        global bot

        self.school_text = self.school_entry.get()
        self.username_text = self.username_entry.get()
        self.password_text = self.password_entry.get()
        try:
            self.rounds_text = int(self.rounds_entry.get())
        except:
            self.rounds_text = 1000000
        self.type_text = self.type.get()
        if self.type_text == 'rockslam' or self.type_text == 'arena' or self.type_text == 'soundcheck':
            self.update_status(f'Sorry! {self.type_text} is not available yet.')
            return None
        self.login = threading.Thread(target = bot.login, args=(self.school_text, self.username_text, self.password_text, self.type_text, self.rounds_text,))
        self.login.start()

    def update_coins(self, coins):
        self.messagecoins = coins
        self.coins_message.set(f'Coins Earned So Far: {coins}')

    def update_status(self, message):
        self.message = message
        self.status_message.set(f'Status: {message}')

    def enable_entry(self):
        self.name_entry.pack(before=self.submit, anchor="w")


    def disable_entry(self):
        self.name_entry.pack_forget()


if __name__ == '__main__':
    driver = None
    bot = Bot()
    gui = Gui()
    gui.mainloop()
