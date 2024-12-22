Amazon Web Scraper

OBJECTIVE : To extract detailed product information from Amazon's Best Sellers section across 10 categories.

Amazon Web Scraping involves extracting data from Amazon's website using tools. In this task, I created a python-based web scraper using selenium that logs into Amazon, which navigates to its Best Sellers section, and extracts product data from 10 selected categories. This mainly focuses on collecting details of products that have discounts and are among the top Best-sellers in each category.

AUTHENTICATION : In this, I used selenium to automate login process with valid Amazon credentials.
-> Navigates through login page securely and handles multi-factor authentication.

DATA COLLECTION : For each product, the scraped attributes are Product Name, Product Price, Sale Discount, Best Seller Rating, Ship From, Sold By, Rating, Product Description, Category Name.
Categories covered in this are Kitchen, Shoes, Computers, Electronics.

DATA STORAGE : The collected data is stored in a structured format(CSV) and organized into columns for easy analysis. 

https://github.com/user-attachments/assets/0816486c-3431-46c4-8ff1-e6e2de60732f
