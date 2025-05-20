from seleniumbase import Driver
from selenium.webdriver.common.by import By
import time

PAGE_URL = "https://www.surfline.com/surf-report/terra-mar-point/5842041f4e65fad6a77088a6"

driver = Driver(uc=True, headless=True)
driver.get(PAGE_URL)
time.sleep(5)   # give the player time to initialize

sources = driver.find_elements(By.TAG_NAME, "source")
print(f"Found {len(sources)} <source> tags:")
for src in sources:
    url = src.get_attribute("src")
    print(" -", url)

driver.quit()
