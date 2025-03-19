import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Test Case 1: The system user enter a valid login information
def test_valid_login():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://katalon-demo-cura.herokuapp.com/")

    driver.find_element(By.XPATH,'//*[@id="menu-toggle"]').click()
    driver.find_element(By.XPATH,'//*[@id="sidebar-wrapper"]/ul/li[3]/a').click()

    driver.find_element(By.ID,'txt-username').send_keys("John Doe")
    driver.find_element(By.ID,'txt-password').send_keys("ThisIsNotAPassword")
    driver.find_element(By.ID,'btn-login').click()
    time.sleep(1)

    driver.find_element(By.XPATH,'//*[@id="menu-toggle"]').click()
    time.sleep(2)
    
    driver.find_element(By.XPATH,'//*[@id="sidebar-wrapper"]/ul/li[4]/a').click()

    profile_page = driver.find_element(By.XPATH,'//*[@id="profile"]/div/div/div/h2')
    assert profile_page.text == "Profile"
    time.sleep(5)

    driver.quit()

#Test Case 2: The system user enter invalid login information
def test_invalid_login():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://katalon-demo-cura.herokuapp.com/")

    driver.find_element(By.XPATH,'//*[@id="menu-toggle"]').click()
    driver.find_element(By.XPATH,'//*[@id="sidebar-wrapper"]/ul/li[3]/a').click()

    driver.find_element(By.ID,'txt-username').send_keys("John Doe")
    driver.find_element(By.ID,'txt-password').send_keys("invalid password")
    driver.find_element(By.ID,'btn-login').click()
    time.sleep(2)

    error_login_message = driver.find_element(By.XPATH,'//*[@id="login"]/div/div/div[1]/p[2]')
    assert error_login_message.text == "Login failed! Please ensure the username and password are valid."

    driver.quit()

#Test Case 3: The system user logout from his account
def test_logout():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://katalon-demo-cura.herokuapp.com/")

    driver.find_element(By.XPATH,'//*[@id="menu-toggle"]').click()
    driver.find_element(By.XPATH,'//*[@id="sidebar-wrapper"]/ul/li[3]/a').click()

    driver.find_element(By.ID,'txt-username').send_keys("John Doe")
    driver.find_element(By.ID,'txt-password').send_keys("ThisIsNotAPassword")
    driver.find_element(By.ID,'btn-login').click()
    time.sleep(1)

    driver.find_element(By.XPATH,'//*[@id="menu-toggle"]').click()
    time.sleep(2)

    driver.find_element(By.XPATH,'//*[@id="sidebar-wrapper"]/ul/li[5]/a').click()
    time.sleep(3)

    driver.find_element(By.XPATH,'//*[@id="menu-toggle"]').click()
    
    login_link = driver.find_element(By.LINK_TEXT,"Login")
    assert login_link.is_displayed(), "Login link is not displayed after logging out."
    time.sleep(3)

    driver.quit()

#Test Case 4: The system user make a valid appointment
def test_make_appointment():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://katalon-demo-cura.herokuapp.com/")

    driver.find_element(By.ID,'btn-make-appointment').click()

    driver.find_element(By.ID,'txt-username').send_keys("John Doe")
    driver.find_element(By.ID,'txt-password').send_keys("ThisIsNotAPassword")
    driver.find_element(By.ID,'btn-login').click()

    WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="combo_facility"]')))
    Select(driver.find_element(By.XPATH,'//*[@id="combo_facility"]')).select_by_visible_text("Hongkong CURA Healthcare Center")
    driver.find_element(By.ID,'chk_hospotal_readmission').click()
    driver.find_element(By.ID,'radio_program_medicaid').click()
    driver.find_element(By.ID,'txt_visit_date').send_keys("01/05/2025")
    time.sleep(2)
    
    driver.find_element(By.ID,'btn-book-appointment').click()
    time.sleep(5)

    appointment_confirmation_title = driver.find_element(By.XPATH,'//*[@id="summary"]/div/div/div[1]/h2')

    appointment_facility = driver.find_element(By.ID,'facility')
    apply_for_hospital_readmission = driver.find_element(By.ID,'hospital_readmission')
    healthcare_program = driver.find_element(By.ID,'program')
    visit_date = driver.find_element(By.ID,'visit_date')

    assert appointment_confirmation_title.text == "Appointment Confirmation"
    assert appointment_facility.text == "Hongkong CURA Healthcare Center"
    assert apply_for_hospital_readmission.text == "Yes"
    assert healthcare_program.text == "Medicaid"
    assert visit_date.text == "01/05/2025"

    driver.quit()

#Test Case 5: The system user make appointments and their appointments displayed in the history tab
def test_display_appointments_in_history_tab():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://katalon-demo-cura.herokuapp.com/")

    driver.find_element(By.ID,'btn-make-appointment').click()

    driver.find_element(By.ID,'txt-username').send_keys("John Doe")
    driver.find_element(By.ID,'txt-password').send_keys("ThisIsNotAPassword")
    driver.find_element(By.ID,'btn-login').click()

    WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="combo_facility"]')))
    Select(driver.find_element(By.XPATH,'//*[@id="combo_facility"]')).select_by_visible_text("Tokyo CURA Healthcare Center")
    driver.find_element(By.ID,'radio_program_medicare').click()
    driver.find_element(By.ID,'txt_visit_date').send_keys("01/10/2025")
    time.sleep(2)
    
    driver.find_element(By.ID,'btn-book-appointment').click()

    WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="summary"]/div/div/div[7]/p/a'))).click()
    time.sleep(2)

    Select(driver.find_element(By.XPATH,'//*[@id="combo_facility"]')).select_by_visible_text("Hongkong CURA Healthcare Center")
    driver.find_element(By.ID,'chk_hospotal_readmission').click()
    driver.find_element(By.ID,'radio_program_medicaid').click()
    driver.find_element(By.ID,'txt_visit_date').send_keys("01/05/2025")
    time.sleep(2)
    
    driver.find_element(By.ID,'btn-book-appointment').click()
    WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="menu-toggle"]'))).click()
    driver.find_element(By.LINK_TEXT,"History").click()

    history_tab_title=driver.find_element(By.XPATH,'//*[@id="history"]/div/div[1]/div/h2')

    appointment1_date=driver.find_element(By.XPATH,'//*[@id="history"]/div/div[2]/div[1]/div/div[1]')
    appointment1_Facility=driver.find_element(By.XPATH,'/html/body/section/div/div[2]/div[1]/div/div[2]/div[2]/p')
    appointment1_hospital_readmission=driver.find_element(By.XPATH,'/html/body/section/div/div[2]/div[1]/div/div[2]/div[5]/p')
    appointment1_Healthcare=driver.find_element(By.XPATH,'/html/body/section/div/div[2]/div[1]/div/div[2]/div[8]/p')

    appointment2_date=driver.find_element(By.XPATH,'//*[@id="history"]/div/div[2]/div[2]/div/div[1]')
    appointment2_Facility=driver.find_element(By.XPATH,'/html/body/section/div/div[2]/div[2]/div/div[2]/div[2]/p')
    appointment2_hospital_readmission=driver.find_element(By.XPATH,'/html/body/section/div/div[2]/div[2]/div/div[2]/div[5]/p')
    appointment2_Healthcare=driver.find_element(By.XPATH,'/html/body/section/div/div[2]/div[2]/div/div[2]/div[8]/p')

    assert history_tab_title.text == "History"

    assert appointment1_date.text == "01/10/2025"
    assert appointment1_Facility.text == "Tokyo CURA Healthcare Center"
    assert appointment1_hospital_readmission.text == "No"
    assert appointment1_Healthcare.text == "Medicare"

    assert appointment2_date.text == "01/05/2025"
    assert appointment2_Facility.text == "Hongkong CURA Healthcare Center"
    assert appointment2_hospital_readmission.text == "Yes"
    assert appointment2_Healthcare.text == "Medicaid"

    driver.quit()