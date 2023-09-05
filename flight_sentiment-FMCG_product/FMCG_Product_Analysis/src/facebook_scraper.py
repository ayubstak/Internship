from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import pandas as pd
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
url = 'https://www.facebook.com/TangoWaferLovers'
driver.get(url)
time.sleep(3)

email = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

email.clear()
email.send_keys("081377019669")
password.clear()
password.send_keys("facebook123,.")

button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[aria-label='Accessible login button']"))).click()
time.sleep(10)

ulasan_button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='https://www.facebook.com/TangoWaferLovers/reviews']"))).click()
# Scroll down the page to load all the reviews
while True:
    try:
        load_more_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Lihat konten lainnya']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
        load_more_button.click()
        time.sleep(2)
    except TimeoutException:
        break

time.sleep(5)

data = []

# Scroll down to load more reviews
SCROLL_PAUSE_TIME = 3

while True:
    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

soup = BeautifulSoup(driver.page_source, "html.parser")
containers = soup.findAll('div', attrs={'class': 'x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z'})
for container in containers:
    review_element = container.find('div', attrs={'class': 'xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs'})
    review_element2 = container.find('div', attrs={'class': 'xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a'})
    if review_element is not None:
        review = review_element.text
        print(review)
        data.append((review))
    if review_element2 is not None:
        review = review_element2.text
        print(review)
        data.append((review))

# Create a DataFrame with "index" starting from 1
df = pd.DataFrame(data, columns=['Review'])
df.index = df.index + 1

# Save DataFrame to a CSV file
df.to_csv('Tango_reviews.csv', index_label='index')
print("Data saved as CSV: diabetasol_reviews.csv")