import pandas as pd
from bs4 import BeautifulSoup

# Load the dataset
file_path = "rekt_data.csv"  # Ensure the correct path
df = pd.read_csv(file_path)

# Drop 'Scammed' column if it exists
if 'Scammed' in df.columns:
    df.drop(columns=['Scammed'], inplace=True)

# Convert 'Date' to datetime format
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Fill missing values with appropriate placeholders
df.fillna({
    'Project Name': 'Unknown',
    'Chain IDs': 'Not Available',
    'Token Name': 'Unknown',
    'Token Addresses': 'Not Available'
}, inplace=True)

# Remove HTML tags from 'Description'
if 'Description' in df.columns:
    df['Description'] = df['Description'].astype(str).apply(lambda x: BeautifulSoup(x, "html.parser").get_text())

# Save the cleaned data to a writable path
df.to_csv("rekt_data_cleaned.csv", index=False)

print("Data cleaning completed. Cleaned file saved as rekt_data_cleaned.csv")
