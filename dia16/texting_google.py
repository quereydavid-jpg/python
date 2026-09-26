from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

recurso = input("Ingrese algo: ")
driver = webdriver.Chrome()
driver.get("http://www.google.com")


web_element = driver.find_element(By.NAME, 'q')
web_element.send_keys("recurso" + Keys.ENTER)
time.sleep(30)