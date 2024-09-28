import re
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def scrape_daraz_product(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode
    chrome_options.add_argument('--no-sandbox')  # Bypass OS security model
    chrome_options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
    chrome_options.add_argument('--disable-gpu')  # Applicable to Windows OS only
    chrome_options.add_argument('--window-size=1920,1080')  # Set window size to prevent errors

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)  # Wait up to 20 seconds

        # Extract title
        try:
            title_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="module_product_title_1"]/div/div/h1')))
            title = title_element.text
        except TimeoutException:
            title = None

        # Extract price
        try:
            price_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="module_product_price_1"]/div/div/span')))
            price_text = price_element.text
            price = parse_price(price_text)
        except TimeoutException:
            price = None

        # Extract rating
        try:
            rating_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="module_product_review_star_1"]/div/a')))
            rating = rating_element.text
        except TimeoutException:
            rating = 'No rating available'

        # Extract details
        try:
            details_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="module_product_detail"]/div/div')))
            details = details_element.text.replace("VIEW MORE", "").strip()
        except TimeoutException:
            details = None

        # Extract images
        try:
            image_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="module_item_gallery_1"]/div/div[1]/div')))
            image_urls = [img.get_attribute('src') for img in image_element.find_elements(By.TAG_NAME, 'img')]
        except TimeoutException:
            image_urls = []

        # Get unique product ID from URL
        daraz_id = extract_daraz_id(url)

        product_data = {
            'name': title,
            'daraz_id': daraz_id,
            'price': price,
            'url': url,
            'image_urls': image_urls,
            'details': details,
            'rating': rating,
        }

        # Save data to CSV
        save_data_to_csv(product_data)

        return product_data

    except Exception as e:
        print(f"Error during scraping: {e}")
        return None

    finally:
        driver.quit()

def parse_price(price_text):
    # Remove currency symbols and commas
    price_text = price_text.replace('৳', '').replace(',', '').strip()
    return float(price_text)

def extract_daraz_id(url):
    # Extract the product ID from the URL
    match = re.search(r'-i(\d+)-s', url)
    return match.group(1) if match else None

def save_data_to_csv(data):
    file_exists = os.path.isfile('product_data.csv')
    with open('product_data.csv', mode='a', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['daraz_id', 'name', 'price', 'url', 'details', 'rating', 'image_urls']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            'daraz_id': data['daraz_id'],
            'name': data['name'],
            'price': data['price'],
            'url': data['url'],
            'details': data['details'],
            'rating': data['rating'],
            'image_urls': ','.join(data['image_urls']),
        })
