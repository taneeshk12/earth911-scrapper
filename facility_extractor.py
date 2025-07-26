import csv
import time
from bs4 import BeautifulSoup
from selenium import webdriver

# Read the CSV links and prepend base URL
def read_links(filename="facility_links.csv"):
    links = []
    with open(filename, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            full_url = "https://search.earth911.com" + row["Facility Link"]
            links.append(full_url)
    return links

# Extract data from each facility page
def extract_facility_data(driver, url):
    driver.get(url)
    time.sleep(3)  # Give the page time to load

    soup = BeautifulSoup(driver.page_source, "html.parser")

    try:
        name = soup.find("h1", class_="back-to noprint").get_text(strip=True)
    except:
        name = ""

    try:
        last_verified = soup.find("span", class_="last-verified").get_text(strip=True)
    except:
        last_verified = ""

    try:
        address = soup.find("div", class_="contact").find("p", class_="addr").get_text(strip=True)
    except:
        address = ""

    try:
        phone = soup.find("div", class_="contact").find("p", class_="phone").get_text(strip=True)
    except:
        phone = ""

    try:
        category = soup.find("div", class_="materials-title").find("h2", class_="accepted").get_text(strip=True)
    except:
        category = ""

    try:
        accepted = soup.select("table.materials-accepted td.material-name")
        accepted_materials = [td.get_text(strip=True) for td in accepted]
    except:
        accepted_materials = []

    return {
        "Facility Name": name,
        "Last Verified": last_verified,
        "Address": address,
        "Phone": phone,
        "Category": category,
        "Accepted Materials": ", ".join(accepted_materials),
        "Source Link": url
    }

# Main scraper logic
def scrape_all_facilities(links):
    driver = webdriver.Chrome()
    all_data = []

    for link in links:
        try:
            print(f"Scraping: {link}")
            data = extract_facility_data(driver, link)
            all_data.append(data)
        except Exception as e:
            print(f"❌ Failed to scrape {link}: {e}")

    driver.quit()

    # Save to CSV
    with open("facility_details.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "Facility Name", "Last Verified", "Address", "Phone", "Category", "Accepted Materials", "Source Link"
        ])
        writer.writeheader()
        writer.writerows(all_data)

    print("✅ All facility data saved to facility_details.csv")

if __name__ == "__main__":
    links = read_links("facility_links.csv")
    scrape_all_facilities(links)
