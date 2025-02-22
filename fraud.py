from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup  
import time
import csv

# Setup Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# CSV File
csv_file = "scraped_data1.csv"
header = ["Title", "URL"]

# Check if file exists before writing the header
try:
    with open(csv_file, 'x', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)  # Write header only once
except FileExistsError:
    pass  # File already exists, skip header writing

# Loop through pages 0 to 32
for page_number in range(0, 33):  # Page 0 to 32
    print(f"🔄 Scraping page {page_number}...")
    driver.get(f"https://rekt.news/?page={page_number}")

    time.sleep(3)  # Wait for JavaScript to load

    # Get page source after JavaScript loads
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    articles = soup.find_all('article', class_='post')

    # Prepare data to append to CSV
    scraped_data = []

    for article in articles:
        title_tag = article.find('h5', class_='post-title')
        if title_tag:
            a_tag = title_tag.find('a')
            if a_tag and a_tag.get('href'):
                title = a_tag.get_text(strip=True)
                url = "https://rekt.news" + a_tag['href']
                scraped_data.append([title, url])  # Append to list

    # Append new data to CSV
    with open(csv_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(scraped_data)

    print(f"✅ Page {page_number} data appended to {csv_file}")

# Close browser
driver.quit()
print("🎉 Scraping completed successfully!")
