from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd

class DarazScraper:
    def __init__(self):
        self.driver = None

    def _initialize_driver(self):
        # Initialize WebDriver without headless option
        self.driver = webdriver.Chrome()

    def _close_driver(self):
        if self.driver:
            self.driver.quit()

    def get_info(self, url):
        try:
            self._initialize_driver()
            self.driver.get(url)
            sleep(5)  # Wait for the page to load

            # Extract title
            title_element = self.driver.find_element(By.CLASS_NAME, 'pdp-product-title')
            title = title_element.text

            # Extract price
            price_element = self.driver.find_element(By.XPATH, '//*[@id="module_product_price_1"]/div/div/span')
            price = price_element.text

            # Extract rating
            rating_element = self.driver.find_element(By.XPATH, '//*[@id="module_product_review"]/div/div/div[2]/div[1]/div[1]/div[1]/span[1]')
            rating = rating_element.text

            # Extract details
            details_element = self.driver.find_element(By.XPATH, '//*[@id="module_product_detail"]')
            details = details_element.text

            # Remove "VIEW MORE" from details
            details = details.replace("VIEW MORE", "").strip()

            # Print the extracted information
            print(f"Title: {title}")
            print(f"Price: {price}")
            print(f"Rating: {rating}")
            print(f"Details: {details}")

            return {
                "Title": title,
                "Price": price,
                "Rating": rating,
                "Details": details
            }
        except Exception as e:
            print(f"Error processing {url}: {e}")
            return None
        finally:
            self._close_driver()

    def scrape_products(self):
        try:
            self._initialize_driver()
            url = "https://www.daraz.com.bd/laptops/"
            self.driver.get(url)
            sleep(5)  # Wait for the page to load

            elements = self.driver.find_elements(By.CLASS_NAME, 'product-card--vHfY9')

            links = []
            data = []
            for element in elements:
                href = element.get_attribute('href')
                if href.startswith("//"):
                    href = "https:" + href
                links.append(href)
                product_data = self.get_info(href)
                if product_data is not None:
                    data.append(product_data)
                else:
                    print(f"Skipping product: {href}")

            # Convert data to pandas DataFrame
            df = pd.DataFrame(data)

            # Save DataFrame to Excel file
            df.to_excel('scraped_data.xlsx', index=False)

            print("Data saved to scraped_data.xlsx")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self._close_driver()
