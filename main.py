from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# Set up Chrome options for headless browsing
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run browser in headless mode (no UI)
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')

driver = None
all_titles = []  # List to store (title, price) tuples
output_filename = "gajmarket_books_with_prices.csv"

start_page = 1  # First page to scrape
end_page = 3    # Last page to scrape
base_url = "https://www.gajmarket.com/%DA%A9%D8%AA%D8%A7%D8%A8-%D8%B9%D9%85%D9%88%D9%85%DB%8C"

try:
    # Start Chrome driver
    print("🛠️ Launching Chrome driver in Headless mode...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    print("✅ Driver launched.")

    # Loop through the desired pages
    for page_num in range(start_page, end_page + 1):
        url = f"{base_url}?page={page_num}"
        print(f"\n🌐 Navigating page {page_num} of {end_page}: {url}")
        driver.get(url)

        try:
            # Wait for product cards to load
            print("⏳ Waiting for product cards to load...")
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.product-card"))
            )
            print("✅ Product cards loaded.")

            product_cards = driver.find_elements(By.CSS_SELECTOR, "article.product-card")

            if not product_cards:
                print(f"⚠️ No products found on page {page_num}.")
            else:
                print(f"📚 Found {len(product_cards)} products on page {page_num}.")
                # Extract title and price for each product
                for card in product_cards:
                    try:
                        title = card.find_element(By.CSS_SELECTOR, "h3.product-card__name").text.strip()
                        price = card.find_element(By.CSS_SELECTOR, "div.product-card__price").text.strip()
                        price = price.replace('تومان', '').strip()
                        price = price.replace(',', '')    
                        all_titles.append((title, price))
                    except Exception as e:
                        print("⚠️ Error extracting title or price of a product:", e)

            time.sleep(1)  # Be polite and avoid hammering the server

        except Exception as page_e:
            print(f"❌ Error navigating or loading page {page_num}:", page_e)

    # Save results to CSV if any data was found
    if all_titles:
        print(f"\n📝 Saving {len(all_titles)} titles with prices to file '{output_filename}'...")
        df = pd.DataFrame(all_titles, columns=["Title", "Price"])
        df.index += 1  # Start index from 1
        df.to_csv(output_filename, encoding="utf-8-sig", sep=";", index_label="No")
        print(f"✅ All data successfully saved to file '{output_filename}'.")
    else:
        print("\n❌ No data found to save.")

except Exception as main_e:
    # Catch any unexpected errors
    print("\n❌ General error during execution:", main_e)

finally:
    # Always close the driver at the end
    if driver:
        driver.quit()
        print("\n✅ Chrome driver closed.")

print("\n📊 Script execution finished.")
