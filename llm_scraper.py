import csv
import json
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

# Load environment variables
groq_api_key = "set your api key"

# Initialize Groq LLM through LangChain
llm = ChatGroq(api_key=groq_api_key, model="llama-3.1-8b-instant")

# Prompt template
TAXONOMY_PROMPT = """
You are a data classifier. Given facility information, convert it into this JSON format:

[
  {{
    "business_name": "...",
    "last_update_date": "...",
    "street_address": "...",
    "materials_category": [...],
    "materials_accepted": [...]
  }}
]

Use the following taxonomy:

Electronics:
- Computers, Laptops, Tablets
- Monitors, TVs (CRT & Flat Screen)
- Cell Phones, Smartphones
- Printers, Copiers, Fax Machines
- Audio/Video Equipment
- Gaming Consoles
- Small Appliances (Microwaves, Toasters, etc.)
- Computer Peripherals (Keyboards, Mice, Cables, etc.)

Batteries:
- Household Batteries (AA, AAA, 9V, etc.)
- Rechargeable Batteries
- Lithium-ion Batteries
- Button/Watch Batteries
- Power Tool Batteries
- E-bike/Scooter Batteries
- Car/Automotive Batteries

Paint & Chemicals:
- Latex/Water-based Paint
- Oil-based Paint and Stains
- Spray Paint
- Paint Thinners and Solvents
- Household Cleaners
- Pool Chemicals
- Pesticides and Herbicides
- Automotive Fluids (Oil, Antifreeze)

Medical Sharps:
- Needles and Syringes
- Lancets
- Auto-injectors (EpiPens)
- Insulin Pens
- Home Dialysis Equipment

Textiles & Clothing:
- Clothing and Shoes
- Household Textiles (Towels, Bedding)
- Fabric Scraps
- Accessories (Belts, Bags, etc.)

Other Important Materials:
- Fluorescent Bulbs and CFLs
- Mercury Thermometers
- Smoke Detectors
- Fire Extinguishers
- Propane Tanks
- Mattresses and Box Springs
- Large Appliances (Fridges, Washers, etc.)
- Construction Debris (Residential Quantities)

Facility Info:
Facility Name: {name}
Last Verified: {date}
Address: {address}
Materials Title: {category}
Accepted Items: {materials}

Return only the JSON.
"""

prompt_template = PromptTemplate(
    input_variables=["name", "date", "address", "category", "materials"],
    template=TAXONOMY_PROMPT
)

# Read from facility_details.csv
def load_facilities(csv_path="facility_details.csv"):
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)

def classify_with_llm(entry):
    prompt = prompt_template.format(
        name=entry["Facility Name"],
        date=entry["Last Verified"],
        address=entry["Address"],
        category=entry["Category"],
        materials=entry["Accepted Materials"]
    )

    response = llm.invoke(prompt)
    try:
        parsed = json.loads(response.content.strip())
    except Exception as e:
        print(f"❌ Error parsing response: {response.content}")
        parsed = None

    return parsed

def main():
    entries = load_facilities()
    final_output = []

    for entry in entries:
        print(f"🔍 Processing: {entry['Facility Name']}")
        result = classify_with_llm(entry)
        if result:
            final_output.extend(result)

    # Save JSON output
    with open("final_structured.json", "w") as f:
        json.dump(final_output, f, indent=2)

    print("✅ Output saved to final_structured.json")

if __name__ == "__main__":
    main()
