import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains

## Scrape for skills mentioned in company job descriptions!

baseLink = 'https://www.tesla.com/careers/search/?department=3'
totalPage = 29
exclusion = ['Fall 2021 Interns_Venkat, Ganesh Engineering & Information Technology Palo Alto, California']

## Init total counter
dictionary = dict()

driver = webdriver.Chrome(executable_path="./chromedriver")
driver.get(baseLink)
time.sleep(0.8)
location = sel = Select(driver.find_element_by_name('/country'))
sel.select_by_index(0)
time.sleep(0.8)

for i in range(totalPage):
    end=driver.find_element_by_class_name("tds-footer-meta")
    a = ActionChains(driver)
    a.move_to_element(end).perform()

WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CLASS_NAME,"tds-table-body")))
rows=driver.find_elements(By.CLASS_NAME, "tds-table-row")
for row in rows[1:]:
    print(row.text)
    if row.text in exclusion:
        continue
    link = row.find_element_by_tag_name('a').get_attribute('href')
    driver2 = webdriver.Chrome(executable_path="./chromedriver")
    driver2.get(link)

    content = driver2.find_element_by_id("app")
    text = content.find_elements(By.TAG_NAME, "li")

    for t in text:
        # print(t.text)
        ## Seperate words that have special characters
        t = t.text.strip().lower().replace("," , " ").replace("/" , " ").split(" ")
        for word in t:
            ## Remove special characters
            w = word.replace("," , "").replace("/" , "").replace(")" , "").replace("(" , "").replace("." , "").replace("!" , "")
            # print(w)
            if w in dictionary:
                dictionary[w] = dictionary[w] + 1
            else:
                dictionary[w] = 1

    driver2.close()
driver.close()

## Write to csv
with open('Tesla.csv', 'w') as f:  
    writer = csv.writer(f)
    for k, v in dictionary.items():
       writer.writerow([k, v])

