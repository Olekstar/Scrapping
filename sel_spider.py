from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Correct the path here
service = Service()
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument("--headless")

with webdriver.Chrome(service=service, options=options) as driver:

    driver.get("https://quotes.toscrape.com/login")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )

    username = driver.find_element(By.ID, "username")
    username.send_keys("admin")

    password = driver.find_element(By.ID, "password")
    password.send_keys("admin")
    #/html/body/div/form/input[2]
    button = driver.find_element(by=By.XPATH, value="html//input[@class='btn btn-primary']")
    button.click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "footer"))
    )
    html = driver.page_source # --> BS
    links = driver.find_elements(by=By.TAG_NAME, value="a")
    [print(link.get_attribute("href")) for link in links]


    sleep(2)




    # driver.quit()