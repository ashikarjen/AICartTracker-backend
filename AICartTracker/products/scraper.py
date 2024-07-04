import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from .models import Product

def scrape_products():
    # Setup the Selenium WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Navigate to the website
    driver.get('https://www.example.com/products')

    # Allow some time for the page to load
    time.sleep(5)

    # Locate and extract product information
    products = driver.find_elements(By.CSS_SELECTOR, '.product-item')
    for item in products:
        name = item.find_element(By.CSS_SELECTOR, '.product-name').text
        price = float(item.find_element(By.CSS_SELECTOR, '.product-price').text.replace('$', ''))
        description = item.find_element(By.CSS_SELECTOR, '.product-description').text
        url = item.find_element(By.CSS_SELECTOR, '.product-link').get_attribute('href')
        Product.objects.create(name=name, price=price, description=description, url=url)

    # Quit the driver
    driver.quit()
