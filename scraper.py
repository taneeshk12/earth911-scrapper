from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import time

# Step 1: Open the page with Selenium
url = "https://search.earth911.com/?what=Electronics&where=10001&list_filter=all&max_distance=100"

# Initialize browser
driver = webdriver.Chrome()
driver.get(url)

# Give time for JS content to load
time.sleep(10)  # adjust if needed

# Step 2: Get page source and parse with BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")

# Step 3: Find all <h2 class="title"> and get <a> tags
links = []
for h2 in soup.find_all("h2", class_="title"):
    a_tag = h2.find("a", href=True)
    if a_tag:
        links.append(a_tag["href"])

driver.quit()

# Step 4: Save to CSV
with open("facility_links.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Facility Link"])
    for link in links:
        writer.writerow([link])

print(f"✅ {len(links)} links saved to facility_links.csv")
