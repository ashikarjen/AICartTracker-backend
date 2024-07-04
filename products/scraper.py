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

    # Navigate to Daraz BD
    driver.get('https://www.daraz.com.bd/')

    # Allow some time for the page to load
    time.sleep(5)

    # Example search for a product category
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys('laptops')
    search_box.submit()

    # Allow some time for search results to load
    time.sleep(5)

    # Locate and extract product information
    products = driver.find_elements(By.CSS_SELECTOR, '.c1_t2i')
    for item in products:
        name = item.find_element(By.CSS_SELECTOR, '.c16H9d a').text
        price = item.find_element(By.CSS_SELECTOR, '.c13VH6').text.replace('৳', '').replace(',', '')
        url = item.find_element(By.CSS_SELECTOR, '.c16H9d a').get_attribute('href')
        description = item.find_element(By.CSS_SELECTOR, '.c1dxR9').text
        
        # Convert price to float
        try:
            price = float(price)
        except ValueError:
            price = 0.0

        # Create or update product in the database
        Product.objects.update_or_create(
            url=url,
            defaults={'name': name, 'price': price, 'description': description}
        )

    # Quit the driver
    driver.quit()
