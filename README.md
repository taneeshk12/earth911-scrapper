# ♻️ LLM-Based Recycling Facility Scraper

This project scrapes recycling center data from [Earth911](https://search.earth911.com/) and uses an LLM (via Groq API) to cleanly structure the data into JSON format, categorized by accepted materials.

---

## 🧾 Files & Their Roles

| File Name              | Purpose |
|------------------------|---------|
| `scraper.py & facility_scraper` | Scrapes facility links from Earth911's search result page using Selenium + BeautifulSoup |
| `facility_links.csv`  | Contains collected facility links from the search result |
| `facility_details.csv`| Full facility info including address, phone, accepted materials |
| `llm_scraper.py`       | Uses LangChain + Groq API to classify materials and generate clean JSON |
| `final_structured.json` | Output file formatted according to the required material taxonomy |
| `.env`                | Stores your GROQ_API_KEY securely (not uploaded to GitHub) |

---

## ✅ Submission Instructions (Simplified & Clear)



### 1. Briefly Explain How You Used the LLM
- **How you guided the LLM to classify the materials**  
  I provided a predefined taxonomy of material categories (like Electronics, Batteries, etc.) and clear examples of acceptable items. Each facility’s information (name, address, materials) was converted into a structured prompt asking the LLM to classify materials accordingly.

- **How your LangChain pipeline works**  
  I used LangChain’s `PromptTemplate` and `ChatGroq` integration. For each facility, a structured prompt was created and sent to Groq's LLM, which returned standardized JSON data.

### 2. Handling Edge Cases
- **Missing or inconsistent data**: The scraper skips empty fields gracefully to avoid crashes.
- **Map-only or JS-loaded content**: Selenium ensures fully rendered content is captured.
- **Vague material names**: LLM intelligently matches them to correct taxonomy items without manual keyword matching.
- 
## 🧠 Example Output Format

```json
[
  {
    "business_name": "Green Earth Recyclers",
    "last_update_date": "2023-11-04",
    "street_address": "123 5th Ave, New York, NY 10001",
    "materials_category": ["Electronics", "Batteries"],
    "materials_accepted": [
      "Computers, Laptops, Tablets",
      "Cell Phones, Smartphones",
      "Lithium-ion Batteries"
    ]
  }
]
