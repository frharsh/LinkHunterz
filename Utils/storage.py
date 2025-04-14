import csv
import pandas as pd

def save_to_csv(url, status):
    with open("scanned_urls.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([url, status])

def check_previous_scans(url):
    try:
        df = pd.read_csv("scanned_urls.csv")
        if url in df.values:
            return "⚠️ This link has been flagged as malicious before!"
    except FileNotFoundError:
        pass
    return None
