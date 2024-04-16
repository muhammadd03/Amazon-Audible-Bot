from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# options = Options()
# options.add_argument('headless')
# options.add_argument('window-size=1920x1080')

driver = webdriver.Chrome()
# add options=options in the paranthesis and comment out the line6-8
driver.get('https://www.audible.com/adblbestsellers?ref_pageloadid=not_applicable&ref=a_search_t1_navTop_pl0cg1c0r0&pf_rd_p=334a4a9c-12d2-4c3f-aee6-ae0cbc6a1eb0&pf_rd_r=EXM30RP56BTAHENN0JKC&pageLoadId=lnInJBw8FSaufH1p&creativeId=7ba42fdf-1145-4990-b754-d2de428ba482')
driver.maximize_window()

#pagination
pagination = driver.find_element(By.XPATH, '//ul[contains(@class, "pagingElements")]')
pages = pagination.find_elements(By.TAG_NAME, 'li')
last_page = int(pages[-2].text)

current_page = 1

book_title = []
book_author = []
book_lenght = []


while current_page <= last_page:
    time.sleep(2)
    container = driver.find_element(By.CLASS_NAME, 'adbl-impression-container ')
    # .//li[contains(@class, "productListItem")]
    products = container.find_elements(By.XPATH, './/li[contains(@class, "productListItem")]')

    for product in products:
        book_title.append(product.find_element(By.XPATH, './/h3[contains(@class, "bc-heading")]').text)
        book_author.append(product.find_element(By.XPATH, './/li[contains(@class, "authorLabel")]').text)
        book_lenght.append(product.find_element(By.XPATH, './/li[contains(@class, "runtimeLabel")]').text)

    current_page = current_page+1
    try:
        next_page = driver.find_element(By.XPATH,  '//span[contains(@class, "nextButton")]')
        next_page.click()
    except:
        pass

driver.quit()

df_books =pd.DataFrame({'Title': book_title, 'Author': book_author, 'Lenght': book_lenght})
df_books.to_csv('Books_headlessTest4withPagination.csv', index=False)

