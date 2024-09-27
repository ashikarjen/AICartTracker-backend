from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def scrape_daraz_product(url):
    # Set up Selenium WebDriver
    options = Options()
    options.headless = True  # Run in headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        
        # Extract title
        title_element = driver.find_element(By.CLASS_NAME, 'pdp-product-title')
        title = title_element.text

        # Extract price
        price_element = driver.find_element(By.XPATH, '//*[@id="module_product_price_1"]/div/div/span')
        price_text = price_element.text
        price = parse_price(price_text)

        # Extract rating
        rating_element = driver.find_element(By.XPATH, '//*[@id="module_product_review"]/div/div/div[2]/div[1]/div[1]/div[1]/span[1]')
        rating = rating_element.text

        # Extract details
        details_element = driver.find_element(By.XPATH, '//*[@id="module_product_detail"]')
        details = details_element.text.replace("VIEW MORE", "").strip()

        # Extract images
        image_elements = driver.find_elements(By.CSS_SELECTOR, 'img.pdp-mod-common-image.gallery-preview-panel__image')
        image_urls = [img.get_attribute('src') for img in image_elements]

        # Get unique product ID from URL or page
        daraz_id = extract_daraz_id(url)

        product_data = {
            'name': title,
            'daraz_id': daraz_id,
            'price': price,
            'url': url,
            'image_urls': image_urls,
            'details': details,
        }

        return product_data

    finally:
        driver.quit()

def scrape_daraz_reviews(url):
    # Implement logic to scrape reviews using Selenium
    # Similar to scrape_daraz_product
    pass

def parse_price(price_text):
    # Remove currency symbols and commas
    price_text = price_text.replace('৳', '').replace(',', '').strip()
    return float(price_text)

def extract_daraz_id(url):
    # Extract the product ID from the URL
    # Example URL: https://www.daraz.com.bd/products/product-name-i123456789.html
    import re
    match = re.search(r'-i(\d+).html', url)
    return match.group(1) if match else None
