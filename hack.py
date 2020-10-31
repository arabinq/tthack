import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import threading
import time

class Bot:
    def __init__(self):
        self.path = 'D:\coding\chromedriver.exe'


    def login(self, school, username, password, type):
        global gui
        global driver

        self.school = school
        self.username = username
        self.password = password
        self.type = type

        gui.update_status('Logging in...')
        driver = webdriver.Chrome(self.path)
        driver.get('https://play.ttrockstars.com/auth/school/student')
        time.sleep(2)
        gui.update_status('Inputting school...')
        self.login_school = driver.find_element_by_xpath('//*[@id="mat-input-0"]')
        self.login_school.send_keys(self.school)
        time.sleep(1)
        self.login_school.send_keys(Keys.RETURN)
        time.sleep(1)
        try:
            self.login_username = driver.find_element_by_xpath('//*[@id="mat-input-1"]')
            gui.update_status('Inputting Username...')
        except:
            driver.quit()
            gui.update_status('Error: Invalid School')
            return None
        self.login_username.send_keys(self.username)
        driver.find_element_by_xpath('/html/body/ttr-root/ttr-root-app/div/div/section/ttr-login2/ttr-splash/div/div/div/ttr-login-form/div/form/mat-card/div[3]/div[2]/button').click()
        gui.update_status('Inputting Password...')
        self.login_password = driver.find_element_by_xpath('//*[@id="mat-input-2"]')
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

        if self.type == 'garage':
            gui.update_status('Going Into Garage Game...')
            self.question_xpath = '/html/body/ttr-root/ttr-root-app/div/div/section/ttr-garage/ttr-game-holder/div/div/div/ttr-game-footpedal/section[2]/section/section/ttr-game-question/span[2]'
            self.play = driver.find_element_by_xpath('/html/body/ttr-root/ttr-root-app/div/div/section/ttr-play-page/section/div/ttr-garage-preview/ttr-game-preview/mat-card/div[1]/div[1]/section/section')
            self.play.click()
        elif self.type == 'festival':
            gui.update_status('Going Into Festival Game...')
            self.question_xpath = '/html/body/ttr-root/ttr-root-app/div/div/section/ttr-festival/ttr-game-holder/div/div/div/ttr-game-footpedal/section[2]/section/section/ttr-game-question/span[2]'
            self.play = driver.find_element_by_xpath('/html/body/ttr-root/ttr-root-app/div/div/section/ttr-play-page/section/div/ttr-festival-preview/ttr-game-preview/mat-card/div[2]/ttr-game-stages/div/div[1]/ttr-game-stage/button')
            self.play.click()
            self.timer = int(driver.find_element_by_xpath('/html/body/ttr-root/ttr-root-app/div/div/section/ttr-play-page/section/div/ttr-festival-preview/ttr-game-preview/mat-card/div[2]/ttr-game-stages/div/div[1]/ttr-game-stage/div').text.strip())
            time.sleep(self.timer)
        gui.update_status('answering questions...')
        while True:
            time.sleep(6)
            self.t_end = time.time() + 60 * 3
            while time.time() < self.t_end:
                time.sleep(0.2)
                try:
                    self.answer = self.parse_question(driver.find_element_by_xpath(self.question_xpath))
                    driver.find_element_by_xpath('/html/body').send_keys(self.answer, Keys.ENTER)
                except:
                    break
            gui.update_status('game ended, going into new game...')
            time.sleep(6)
            self.play_again = driver.find_element_by_xpath('/html/body/ttr-root/ttr-root-app/div/div/section/ttr-garage/ttr-game-holder/div/div/div/button[2]')
            self.play_again.click()

        gui.update_status('Hack ended...')

    def parse_question(self, location):
        self.location = location
        self.text = self.location.text
        self.word_list = self.text.split()
        if '÷' in self.text:
            self.ans = int(int(self.word_list[0]) / int(self.word_list[2]))
        elif '×' in self.text:
            self.ans = int(int(self.word_list[0]) * int(self.word_list[2]))
        return str(self.ans)

    def end(self):
        global driver
        driver.quit()
        gui.update_status('Ended Hack.')
        return None


class Gui:
    def __init__(self):
        pass

    def draw(self):
        global root
        global bot

        if not root:
            root  = tk.Tk()
            root.geometry('300x300')

            self.type = tk.StringVar()
            self.status_message = tk.StringVar()
            self.school_label = tk.Label(text="School")
            self.school_entry = tk.Entry()
            self.username_label = tk.Label(text="Username")
            self.username_entry = tk.Entry()
            self.password_label = tk.Label(text="Password")
            self.password_entry = tk.Entry()
            self.type_label = tk.Label(text="Game Mode")
            self.type_entry_one = tk.Radiobutton(text="Garage", value="garage", variable=self.type)
            self.type_entry_two = tk.Radiobutton(text="Festival", value="festival", variable=self.type)
            self.submit = tk.Button(text="Start Hack", command=self.send_values)
            self.end = tk.Button(text="End Hack", command=bot.end)
            self.status = tk.Label(textvariable=self.status_message)
            self.status_message.set('Waiting...')
            self.school_label.pack()
            self.school_entry.pack()
            self.username_label.pack()
            self.username_entry.pack()
            self.password_label.pack()
            self.password_entry.pack()
            self.type_label.pack()
            self.type_entry_one.pack()
            self.type_entry_two.pack()
            self.submit.pack()
            self.end.pack()
            self.status.pack()

            root.mainloop()

    def send_values(self):
        global bot

        self.school_text = self.school_entry.get()
        self.username_text = self.username_entry.get()
        self.password_text = self.password_entry.get()
        self.type_text = self.type.get()
        print(self.type_text)
        self.login = threading.Thread(target = bot.login, args=(self.school_text, self.username_text, self.password_text, self.type_text,))
        self.login.start()


    def update_status(self, message):
        self.message = message
        self.status_message.set(message)




if __name__ == '__main__':
    driver = None
    root = None
    bot = Bot()
    gui = Gui()
    gui.draw()
