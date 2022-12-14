import datetime
import Modes
import settings as s
from selenium import webdriver
import securepassword

def main():
    print("===================Speed Enroller v2=====================")
    s.testMode = True if input("Test Mode? (y/n): ") == 'y' else False
    if s.testMode:
        s.id = "id"
        s.pw = "password"
        s.targetTime = datetime.datetime.now() + datetime.timedelta(minutes=1.5)
        s.CLICKTEXT = "Cancel"
        devmode = "exe"
    else:
        s.id = input("ERAU login ID: ")
        s.pw = securepassword.getpass("ERAU login PW: ")
        now = datetime.datetime.now()
        goal = datetime.datetime.strptime(input("Target Time (HH:MM): "), "%H:%M")
        s.targetTime = datetime.datetime(now.year, now.month, now.day, goal.hour, goal.minute, 0)
        devmode = input("Input developer code or press enter to continue: ")
        s.CLICKTEXT = "Continue"
    print("=========================================================")

    print("Starting web driver...")
    driver = webdriver.Firefox()
    print("Web driver started.")

    if devmode == "exe":
        if (Modes.DevMode(driver) < 0):
            if input("Process failed, retry (y/n)? ") == 'y':
                main()
    else:
        Modes.StandardMode(driver)

if __name__ == '__main__':
    main()