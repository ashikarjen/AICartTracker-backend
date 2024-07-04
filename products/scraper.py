import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from .models import Product

def scrape_products():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get('https://www.daraz.com.bd/')

    time.sleep(5)

    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys('laptops')
    search_box.submit()

    time.sleep(5)

    products = driver.find_elements(By.CSS_SELECTOR, '.c2prKC')
    for item in products:
        try:
            name = item.find_element(By.CSS_SELECTOR, '.c16H9d a').text
            price = item.find_element(By.CSS_SELECTOR, '.c3gUW0').text.replace('৳', '').replace(',', '')
            url = item.find_element(By.CSS_SELECTOR, '.c16H9d a').get_attribute('href')
            description = 'No description available'

            price = float(price)

            print(f"Scraped product: {name}, {price}, {url}, {description}")

            # Check if the product is created successfully
            product, created = Product.objects.update_or_create(
                url=url,
                defaults={'name': name, 'price': price, 'description': description}
            )
            if created:
                print(f"Created new product: {name}")
            else:
                print(f"Updated existing product: {name}")

        except Exception as e:
            print(f"Error scraping product: {e}")

    driver.quit()
