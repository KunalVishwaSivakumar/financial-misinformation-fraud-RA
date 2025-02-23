import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

def create_folders():
    os.makedirs("html_files", exist_ok=True)
    os.makedirs("text_files", exist_ok=True)

def fetch_and_save_html(url, folder):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            filename = url.split("/")[-2] + ".html"
            file_path = os.path.join(folder, filename)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(response.text)
            return file_path
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return None

def extract_text_from_html(html_file, text_folder):
    try:
        with open(html_file, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")
            text = soup.get_text(separator="\n", strip=True)
            
            text_filename = os.path.basename(html_file).replace(".html", ".txt")
            text_path = os.path.join(text_folder, text_filename)
            
            with open(text_path, "w", encoding="utf-8") as txt_file:
                txt_file.write(text)
    except Exception as e:
        print(f"Error processing {html_file}: {e}")

def main(csv_file):
    create_folders()
    df = pd.read_csv('scraped_data.csv')
    urls = df["URL"].dropna().tolist()
    
    html_folder = "html_files"
    text_folder = "text_files"
    
    for i, url in enumerate(urls):
        print(f"Processing {i+1}/{len(urls)}: {url}")
        html_file = fetch_and_save_html(url, html_folder)
        if html_file:
            extract_text_from_html(html_file, text_folder)
        time.sleep(2)  # Adding a delay to prevent getting blocked
    
    print("Processing complete. Check 'html_files' and 'text_files' folders.")

if __name__ == "__main__":
    csv_file = "scraped_data.csv"  # Ensure this file is in the same directory
    main(csv_file)
