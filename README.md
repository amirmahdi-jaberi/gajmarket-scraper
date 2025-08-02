# Gaj Market Scraper

This script uses Selenium to collect information about books from the Gaj Market website and saves their titles and prices in a CSV file.

## Features
- Extracts book titles and prices from different pages of the Gaj Market website
- Saves the data in the `gajmarket_books_with_prices.csv` file
- Automatically runs Google Chrome in headless mode (without UI)

## Prerequisites
- Python 3.7 or higher
- Google Chrome

### Recommended library versions
- selenium: 4.15.2
- webdriver-manager: 3.8.6
- pandas: 2.2.2

## Install Dependencies
First, install the required dependencies using the following command:

```
pip install -r requirements.txt
```

## How to Run

1. Run the `main.py` file:

```
python main.py
```

2. After execution, the output file `Sample-data-extracted.csv` will be created in the same folder.

## Settings
- The number of pages to scrape can be changed via the `start_page` and `end_page` variables at the top of the code.
- The main books page URL is set in the `base_url` variable.

## Important Notes
- To avoid being blocked by the website, a one-second delay is set between each page.
- If you encounter issues running the script or installing the Chrome driver, make sure you have the latest version of Google Chrome installed on your system.

---

Prepared by Amir Jaberi 
