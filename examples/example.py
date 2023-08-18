from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from win32com.client import Dispatch
import time

import CourseBot

if __name__ == "__main__":
    registered = False
    errors = 0
    #keep trying until we successfully register or until bot runs into error 10 times in a row
    while registered == False and errors < 10:
        try:
            #start edge
            driver = webdriver.Edge()
            #initialize wait
            wait = WebDriverWait(driver, 10)
            #login with proper netid, password
            CourseBot.login(driver, wait, 'mynetid', 'mypassword')
            #wait until searchbar is loaded in
            wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/main/div[3]/div/div[2]/div/div[1]/div/div[1]/div[3]/div[1]/div/fieldset/div[1]/p/div/ul/li/input")))
            #search for course
            CourseBot.course_search(driver, 'computer science', '225')
            #wait for next button to be clickable
            wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/div[3]/div/div[2]/div/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[1]/div[2]/div/button[3]")))
            #find next button
            next_button = driver.find_element(By.XPATH, "/html/body/main/div[3]/div/div[2]/div/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[1]/div[2]/div/button[3]")
            next_button.click()
            #wait for new information to load in
            time.sleep(1)
            #get lecture capacity
            lecture_status = driver.find_element(By.XPATH, "/html/body/main/div[3]/div/div[2]/div/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[1]/div[1]/div/table/tbody/tr[2]/td[9]")
            #if lecture isn't full, add/drop necessary courses
            if 'FULL' not in lecture_status.get_attribute('title'):
                #add desired lecture section
                lecture_add = driver.find_element(By.XPATH, "/html/body/main/div[3]/div/div[2]/div/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[1]/div[1]/div/table/tbody/tr[2]/td[11]/div/button")
                lecture_add.click()
                #wait for addition to register
                time.sleep(1)
                prev_button = driver.find_element(By.XPATH, "/html/body/main/div[3]/div/div[2]/div/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[1]/div[2]/div/button[2]")
                prev_button.click()
                #wait for new information to load in
                time.sleep(1)
                #add desired discussion
                discussion_add = driver.find_element(By.XPATH, "/html/body/main/div[3]/div/div[2]/div/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[1]/div[1]/div/table/tbody/tr[2]/td[11]/div/button")
                discussion_add.click()
                #wait for addition to register
                time.sleep(1)
                #drop lab that conflicts with course we want to add MAKE SURE XPATH IS PATH THAT COURSE WILL BE AFTER ADDING NEW COURSE, OTHERWISE THE WRONG COURSE WILL BE DROPPED
                programming_lab_select = driver.find_element(By.XPATH, "/html/body/main/div[5]/div[1]/div/div[4]/div[1]/div/div[1]/div/table/tbody/tr[5]/td[7]/select")
                #change html so we can interact with select element
                driver.execute_script("arguments[0].setAttribute('style', '')", programming_lab_select)
                time.sleep(0.5)
                Select(programming_lab_select).select_by_value("DW")
                time.sleep(0.5)
                #drop lecture that conflicts with course we want to add MAKE SURE XPATH IS PATH THAT COURSE WILL BE AFTER ADDING NEW COURSE, OTHERWISE THE WRONG COURSE WILL BE DROPPED
                programming_lecture_select = driver.find_element(By.XPATH, "/html/body/main/div[5]/div[1]/div/div[4]/div[1]/div/div[1]/div/table/tbody/tr[6]/td[7]/select")
                #change html so we can interact with select element
                driver.execute_script("arguments[0].setAttribute('style', '')", programming_lecture_select)
                time.sleep(0.5)
                Select(programming_lecture_select).select_by_value("DW")
                time.sleep(0.5)
                #save changes
                saveButton = driver.find_element(By.ID, "saveButton")
                saveButton.click()
                registered = True
                #send success email
                CourseBot.success_email('email')
            #quit driver once execution finishes
            driver.quit()
            #reset errors to 0 if script executes all the way
            errors = 0
        except:
            driver.quit()
            errors += 1

    #send failure email if while loop exited due to errors
    if errors >= 10:
        CourseBot.failure_email('email')