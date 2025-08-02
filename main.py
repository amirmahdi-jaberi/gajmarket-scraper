from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# Configure Chrome options for headless operation
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--start-maximized")
options.add_argument("--disable-gpu")

driver = None
book_data = []  # List to store (title, price) tuples
output_filename = "gajmarket_books_with_prices.csv"

# Each page contains information for 32 books.
start_page = 1
end_page = 3
base_url = "https://www.gajmarket.com/%DA%A9%D8%AA%D8%A7%D8%A8-%D8%B9%D9%85%D9%88%D9%85%DB%8C"

try:
    print("Launching Chrome driver in headless mode...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    print("Driver launched.")

    for page_num in range(start_page, end_page + 1):
        url = f"{base_url}?page={page_num}"
        print(f"Processing page {page_num} of {end_page}: {url}")
        driver.get(url)

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.product-card"))
            )

            product_cards = driver.find_elements(By.CSS_SELECTOR, "article.product-card")

            if not product_cards:
                print(f"No products found on page {page_num}.")
                continue

            print(f"Found {len(product_cards)} products on page {page_num}.")

            for card in product_cards:
                try:
                    title = card.find_element(By.CSS_SELECTOR, "h3.product-card__name").text.strip()
                    price = card.find_element(By.CSS_SELECTOR, "div.product-card__price").text.strip()
                    price = price.replace('تومان', '').replace(',', '').strip()
                    book_data.append((title, price))
                except Exception as e:
                    print("Error extracting product details:", e)

            time.sleep(1)  # Polite delay between requests

        except Exception as page_error:
            print(f"Error loading page {page_num}:", page_error)

    if book_data:
        print(f"Saving {len(book_data)} records to '{output_filename}'...")
        df = pd.DataFrame(book_data, columns=["Title", "Price"])
        df.index += 1
        df.to_csv(output_filename, encoding="utf-8-sig", sep=";", index_label="No")
        print(f"Data saved to '{output_filename}'.")
    else:
        print("No data to save.")

except Exception as e:
    print("General execution error:", e)

finally:
    if driver:
        driver.quit()
        print("Chrome driver closed.")

print("Script execution completed.")
