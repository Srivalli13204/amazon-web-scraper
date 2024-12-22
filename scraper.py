import os
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Initialize WebDriver
def init_driver():
    chrome_driver_path = "C:/Users/sriva/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"  # Replace with the actual path to your chromedriver
    service = Service(chrome_driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    return webdriver.Chrome(service=service, options=options)

# Amazon Login
def amazon_login(driver):
    driver.get("https://www.amazon.in")
    
    try:
        # Click the Sign-In button
        sign_in_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "nav-link-accountList"))
        )
        sign_in_button.click()

        # Enter email
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ap_email"))
        )
        email_input.send_keys(os.getenv("AMAZON_EMAIL", "isiri1320@gmail.com"))  # Securely load from environment variable
        driver.find_element(By.ID, "continue").click()

        # Enter password
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ap_password"))
        )
        password_input.send_keys(os.getenv("AMAZON_PASSWORD", "Srivalli@04"))  # Securely load from environment variable
        driver.find_element(By.ID, "signInSubmit").click()

        print("Login successful!")
    except TimeoutException as e:
        print("Login failed: Timeout while waiting for elements.")
        driver.quit()
    except Exception as e:
        print(f"Login failed: {e}")
        driver.quit()

# Scrape a single category
def scrape_category(driver, category_url, category_name, output_file):
    driver.get(category_url)
    time.sleep(3)

    products = []
    try:
        for page in range(1, 4):  # Adjust range for more pages
            print(f"Scraping page {page} for {category_name}...")
            product_elements = driver.find_elements(By.CSS_SELECTOR, "div.zg-grid-general-faceout")

            for product in product_elements:
                try:
                    name = product.find_element(By.CSS_SELECTOR, "div.p13n-sc-truncate-desktop-type2").text
                    price = product.find_element(By.CSS_SELECTOR, "span.p13n-sc-price").text
                    discount = "N/A"  # Placeholder, replace if discount is available
                    rating = product.find_element(By.CSS_SELECTOR, "span.a-icon-alt").text
                    ship_from = "N/A"  # Placeholder
                    sold_by = "N/A"  # Placeholder
                    product_desc = "N/A"  # Placeholder

                    products.append([name, price, discount, rating, ship_from, sold_by, product_desc, category_name])
                except NoSuchElementException:
                    print("Some product details are missing, skipping...")

            # Navigate to the next page
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, "li.a-last a")
                next_button.click()
                time.sleep(2)
            except NoSuchElementException:
                print("No more pages in this category.")
                break

    except Exception as e:
        print(f"An error occurred while scraping {category_name}: {e}")

    # Write to CSV
    with open(output_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(products)

# Main function
def main():
    driver = init_driver()

    try:
        amazon_login(driver)

        categories = {
            "Kitchen": "https://www.amazon.in/gp/bestsellers/kitchen/ref=zg_bs_nav_kitchen_0",
            "Shoes": "https://www.amazon.in/gp/bestsellers/shoes/ref=zg_bs_nav_shoes_0",
            "Computers": "https://www.amazon.in/gp/bestsellers/computers/ref=zg_bs_nav_computers_0",
            "Electronics": "https://www.amazon.in/gp/bestsellers/electronics/ref=zg_bs_nav_electronics_0"
        }

        output_file = "amazon_best_sellers.csv"
        
        # Create CSV header
        if not os.path.exists(output_file):
            with open(output_file, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([ "Product Name", "Product Price", "Sale Discount", "Best Seller Rating",
                                  "Ship From", "Sold By", "Product Description", "Category Name"])

        # Scrape each category
        for category_name, category_url in categories.items():
            scrape_category(driver, category_url, category_name, output_file)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()