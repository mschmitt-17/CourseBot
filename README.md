# CourseBot
A simple bot I created using WebDriver to register a user for a UIUC course. In CourseBot.py several helper functions are provided, in example.py an example is provided.
Following is a step-by-step explanation of the example code with visuals, as I felt it was rather confusing.

![image link](https://github.com/mschmitt-17/CourseBot/tree/main/imgs/loginscreen.png)

Line:   CourseBot.login(driver, wait, 'mynetid', 'mypassword')

Explanation:    Log in to UIUC self-service and navigate to registration for most recent term


![image link](https://github.com/mschmitt-17/CourseBot/tree/main/imgs/registrationscreen.png)

Lines:  wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/main/div[3]/div/div[2]/div/div[1]/div/div[1]/div[3]/div[1]/div/fieldset/div[1]/p/div/ul/li/input")));
        
        CourseBot.course_search(driver, 'computer science', '225')

Explanation:    pass 'computer science' into subject search bar in image and '225' into CRN search bar in image and search


![image link](https://github.com/mschmitt-17/CourseBot/tree/main/imgs/nextbutton.png)

Lines:  
        wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/div[3]/div/div[2]/div/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[1]/div[2]/div/button[3]")));
        
        next_button = driver.find_element(By.XPATH, "/html/body/main/div[3]/div/div[2]/div/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[1]/div[2]/div/button[3]");
        
        next_button.click();
        
        time.sleep(1)

Explanation:    wait until we can click next button indicated in image, then click the button to move to the next page


![image link](https://github.com/mschmitt-17/CourseBot/tree/main/imgs/classcapacity.png)

Lines:  lecture_status = driver.find_element(By.XPATH, "/html/body/main/div[3]/div/div[2]/div/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[1]/div[1]/div/table/tbody/tr[2]/td[9]")

Explanation:    get element with lecture status indicated by arrow in image, we will use this to determine if the course is full or not; if course is full execution stops here, but we'll assume it isn't


![image link](https://github.com/mschmitt-17/CourseBot/tree/main/imgs/prevbutton.png)

Lines:  if 'FULL' not in lecture_status.get_attribute('title'):
        
        lecture_add = driver.find_element(By.XPATH, "/html/body/main/div[3]/div/div[2]/div/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[1]/div[1]/div/table/tbody/tr[2]/td[11]/div/button");
        
        lecture_add.click();
        
        time.sleep(1);
        
        prev_button = driver.find_element(By.XPATH, "/html/body/main/div[3]/div/div[2]/div/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[1]/div[2]/div/button[2]");
        
        prev_button.click();
        
        time.sleep(1)

Explanation:    if lecture is not full, add the course by pressing the add button on the far right of the screenshot (found by xpath); wait for this to register, then press the button
                to go to the previous screen indicated by the arrow in the image; give this button press time to register as well
                #add desired discussion


![image link](https://github.com/mschmitt-17/CourseBot/tree/main/imgs/addcourse.png)

Lines:  discussion_add = driver.find_element(By.XPATH, "/html/body/main/div[3]/div/div[2]/div/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[1]/div[1]/div/table/tbody/tr[2]/td[11]/div/button");
        
        discussion_add.click();
        
        time.sleep(1)

Explanation:    add discussion section by pressing the add button indicated by the arrow in the attached screenshot; give this press enough time to register


![image link](https://github.com/mschmitt-17/CourseBot/tree/main/imgs/edithtml.png)

Lines:  programming_lab_select = driver.find_element(By.XPATH, "/html/body/main/div[5]/div[1]/div/div[4]/div[1]/div/div[1]/div/table/tbody/tr[5]/td[7]/select");
        
        driver.execute_script("arguments[0].setAttribute('style', '')", programming_lab_select);
        
        time.sleep(0.5)

Explanation:    we must remove courses to make sure the course we want to add doesn't have a time conflict, however the way the website is formatted the select element allowing us to drop courses
                is hidden; we find this element by xpath and execute a script to change the html of this select element so that it is no longer hidden; we can now see the element as the three dots
                indicated by the arrow in the image; give this change enough time to register


![image link](https://github.com/mschmitt-17/CourseBot/tree/main/imgs/removecourse.png)

Lines:  Select(programming_lab_select).select_by_value("DW");
        
        time.sleep(0.5)

Explanation:    now that we can interact with the select element, change it to the value that corresponds to dropping the course; give this enough time to register


![image link](https://github.com/mschmitt-17/CourseBot/tree/main/imgs/removesecondcourse.png?raw=true)

Lines:  programming_lecture_select = driver.find_element(By.XPATH, "/html/body/main/div[5]/div[1]/div/div[4]/div[1]/div/div[1]/div/table/tbody/tr[6]/td[7]/select");
        
        driver.execute_script("arguments[0].setAttribute('style', '')", programming_lecture_select);
        
        time.sleep(0.5);
        
        Select(programming_lecture_select).select_by_value("DW");
        
        time.sleep(0.5)

Explanation:    do the same thing as before for a second conflicting course


![image link](https://github.com/mschmitt-17/CourseBot/tree/main/imgs/submit.png?raw=true)

Lines:  saveButton = driver.find_element(By.ID, "saveButton");
        
        saveButton.click()

Explanation:    click save button indicated by arrow in image; this should save the changes performed by the script, getting us the course we want and removing the conflicting courses
