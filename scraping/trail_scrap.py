from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# /home/kyrylo/filesOfPrograms/geckodriver

driver = webdriver.Firefox()
driver.get('https://www.komoot.com/discover')

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "css-1y2vksk"))
    )
    button = driver.find_element(By.CLASS_NAME, 'css-1y2vksk')
    button.click()
except:
    driver.quit()

field = driver.find_element(By.CLASS_NAME, 'css-1jg5xpk')
field.send_keys("West Highland ways\n")

submit_button = driver.find_element(By.CLASS_NAME, 'css-1ktt71q')
submit_button.click()
