import datetime
import logging as log
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import main
import settings as s


def DevMode(driver):
    for i in range(s.DEV_TABS):
        if i != 0:
            driver.switch_to.new_window('tab')
        driver.get("https://erau.collegescheduler.com/entry")

        if login(driver) < 0:
            return -1

        try:
            element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Shopping Cart']")))
        except:
            log.error("Duo authentication timed out or failed")
            driver.quit()
            return -1
        element.click()
        
        try:
            element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Register']")))
        except:
            log.error("Register Click Failed")
            driver.quit()
            return -1
        element.click()

    
    delta = 5 / (s.DEV_TABS - 3)
    split = 5

    for i in range(s.DEV_TABS):
        driver.switch_to.window(driver.window_handles[i])
        timeleft = 0
        while (datetime.datetime.now() < s.targetTime - datetime.timedelta(seconds=split)):
            sleep(.0001)
            newTimeleft = datetime.timedelta(seconds = (s.targetTime - datetime.datetime.now()).seconds)
            if newTimeleft != timeleft:
                timeleft = newTimeleft
                print(f"Time left: {timeleft.seconds} seconds")
        split -= delta

        driver.find_element_by_xpath(f"//button[text()='{s.CLICKTEXT}']").click()

    sleep(60)

    return 0

def login(driver):
    try:
        element = WebDriverWait(driver, s.SHOPPING_CART_DELAY).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Log In']")))
    except:
        if (not driver.find_element_by_xpath("//span[text()='Shopping Cart']")):
            log.error("Log in button not found")
            driver.quit()
            return -1
        else:
            return 0
    driver.find_element_by_id("username").send_keys(s.id)
    driver.find_element_by_id("inputPassword").send_keys(s.pw)
    element.click()
    return 0


def StandardMode(driver):
    classes = int(input("how many classes to enroll? "))
    driver.get("https://sis.erau.edu/psc/eracsprd_6/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_MD_SP_FL.GBL?Action=U&MD=Y&GMenu=SSR_STUDENT_FL&GComp=SSR_START_PAGE_FL&GPage=SSR_START_PAGE_FL&scname=CS_SSR_MANAGE_CLASSES_NAV")

    while (datetime.datetime.now() < s.targetTime):
        sleep(.0001)

    driver.refresh()
    try:
        element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "DERIVED_REGFRM1_SSR_SELECT$0")))
    except:
        log.error("Checkmark not found")
        return -1
    
    for i in range(classes):
        element = f"//*[@id=\"DERIVED_REGFRM1_SSR_SELECT${i}\"]"
        driver.find_element_by_xpath(element).click()
    
    while (driver.find_element_by_id("DERIVED_SSR_FL_SSR_ENROLL_FL")):
        driver.find_element_by_id("DERIVED_SSR_FL_SSR_ENROLL_FL").click()

    sleep(60)



if __name__ == '__main__':
    main.main()