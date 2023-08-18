from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from win32com.client import Dispatch
import time

#INPUTS:        email - email address to send success email to; user must have outlook set up on their PC for this function to work
#OUTPUTS:       none
#DESCRIPTION:   sends an email to the passed email address informing user the bot has succeeded
def success_email(email):
    #connect with outlook
    outlook = Dispatch('outlook.application')
    #create new email
    mail = outlook.CreateItem(0)
    #send email to passed address
    mail.To = email
    #populate email
    mail.Subject = 'Registration Success'
    mail.Body = 'Successfully registered for course'
    #send email
    mail.Send()

#INPUTS:        email - email address to send failure email to; user must have outlook set up on their PC for this function to work
#OUTPUTS:       none
#DESCRIPTION:   sends an email to the passed email address informing user the bot has failed
def failure_email(email):
    #connect with outlook
    outlook = Dispatch('outlook.application')
    #create new email
    mail = outlook.CreateItem(0)
    #send email to passed address
    mail.To = email
    #populate email
    mail.Subject = 'Bot Failure'
    mail.Body = 'Bot has failed'
    #send email
    mail.Send()

#INPUTS:        driver - webdriver instance the user instantiates; wait - the WebDriverWait instance the user instantiates (used for timing purposes); netid - the user's UIUC netid (I swear I'm not collecting these);
#               password - the user's password (I swear I'm not collecting these); termname - the term the user wishes to register for, passed in the form "Season YYYY" (i.e. Fall 2023), defaults to most recent term
#               available for registration if no argument is passed
#OUTPUTS:       none
#DESCRIPTION:   logs the user in to the UIUC registration system and brings them to the term they wish to register for
def login(driver, wait, netid, password, termname = ""):
    #start on login page
    driver.get('https://login.uillinois.edu/auth/SystemLogin/sm_login.fcc?TYPE=33554433&REALMOID=06-a655cb7c-58d0-4028-b49f-79a4f5c6dd58&GUID=&SMAUTHREASON=0&METHOD=GET&SMAGENTNAME=-SM-dr9Cn7JnD4pZ%2fX9Y7a9FAQedR3gjL8aBVPXnJiLeXLOpk38WGJuo%2fOQRlFkbatU7C%2b9kHQgeqhK7gmsMW81KnMmzfZ3v0paM&TARGET=-SM-HTTPS%3a%2f%2fwebprod%2eadmin%2euillinois%2eedu%2fssa%2fservlet%2fSelfServiceLogin%3fappName%3dedu%2euillinois%2eaits%2eSelfServiceLogin%26dad%3dBANPROD1')
    #fill in netid
    netid_element = driver.find_element(By.ID, 'netid')
    netid_element.send_keys(netid)
    #fill in password
    password_element = driver.find_element(By.ID, 'easpass')
    password_element.send_keys(password)
    #submit form
    password_element.submit()
    #find registration and records link and click it
    link = driver.find_element(By.LINK_TEXT, "Registration & Records")
    link.click()
    #store current window handle, since we will need to switch windows
    registration_menu_handle = driver.current_window_handle
    #find enhanced registration link and click it
    link = driver.find_element(By.LINK_TEXT, "Enhanced Registration")
    link.click()
    #wait until we have 2 windows open
    wait.until(EC.number_of_windows_to_be(2))
    #switch to new window by checking that it's not the same as the last window
    for window_handle in driver.window_handles:
        if window_handle != registration_menu_handle:
            driver.switch_to.window(window_handle)
    #wait until new window loads in
    wait.until(EC.presence_of_element_located((By.ID, "registerLink")))
    #click link to register
    link = driver.find_element(By.ID, "registerLink")
    link.click()
    #wait until new window loads in
    wait.until(EC.title_is("Select a Term"))
    #click term menu to get terms to populate
    term_menu = driver.find_element(By.ID, "s2id_txt_term")
    term_menu.click()
    #if argument is passed for registration term, we have a bit more work to do
    if (termname != ""):
        #wait a bit for terms to populate
        time.sleep(0.5)
        #find all labels which contain term names
        term_options = driver.find_elements(By.CLASS_NAME, "select2-result-label")
        #iterate through all labels
        for item in term_options:
            #unhighlight all parent elements to labels, as this determines which term gets selected
            driver.execute_script("arguments[0].setAttribute('class', 'select2-results-dept-0 select2-result select2-result-selectable')", item.find_element(By.XPATH, '..'))
            #get element one below label (this contains the term name itself)
            term = item.find_element(By.XPATH, ".//*")
            #if term name matches the passed term name, select it and break out of loop
            if termname in term.get_attribute('innerHTML'):
                driver.execute_script("arguments[0].setAttribute('class', 'select2-results-dept-0 select2-result select2-result-selectable select2-highlighted')", item.find_element(By.XPATH, '..'))
                break
    #press enter on searchbar; this will lock in the term we had highlighted in the previous step (most recent term is automatically highlighted)
    searchbar = driver.find_element(By.XPATH, "/html/body/div[8]/div/input")
    time.sleep(1)
    searchbar.send_keys(Keys.RETURN)
    #press continue button
    continue_button = driver.find_element(By.ID, "term-go")
    #this press will occasionally not register unless we wait a little
    time.sleep(0.5)
    continue_button.click()

#INPUTS:        driver - webdriver instance the user instantiates; subject - the subject the user wishes to register for, should be passed how it appears on the registration website for optimal results
#               (i.e. 'computer science' instead of just 'computer' or 'CS'); CRN - the CRN of the class the user wishes to register for
#OUTPUTS:       none
#DESCRIPTION:   searches for course user wants to register for according to passed subject and CRN
def course_search(driver, subject, CRN):
    #find subject searchbar
    subject_searchbar = driver.find_element(By.XPATH, "/html/body/main/div[3]/div/div[2]/div/div[1]/div/div[1]/div[3]/div[1]/div/fieldset/div[1]/p/div/ul/li/input")
    subject_searchbar.send_keys(subject)
    #sleep for a half second, otherwise enter won't register
    time.sleep(1)
    #press enter key
    subject_searchbar.send_keys(Keys.RETURN)
    #find crn searchbar
    crn_searchbar = driver.find_element(By.XPATH, "/html/body/main/div[3]/div/div[2]/div/div[1]/div/div[1]/div[3]/div[1]/div/fieldset/div[1]/p/input[2]")
    crn_searchbar.send_keys(CRN)
    #wait a half second, otherwise enter won't register
    time.sleep(1)
    #press enter key
    crn_searchbar.send_keys(Keys.RETURN)