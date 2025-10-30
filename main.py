from flask import Flask, jsonify, request
from flask_cors import CORS
from google import genai
import os, json, re
from dotenv import load_dotenv

# Load .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Google GenAI client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

EXTRACTION_PROMPT = """
You are an expert real-estate data extractor.

Convert the following property details into a structured JSON object using the exact format below.

### JSON Structure

{
"propertyDetails": [
{
"propertytype": "",
"listingtype": "",
"title": "",
"price": 0.0000,
"deposit": 0.0000,
"maintenance": 0.0000,
"location": "",
"city": "",
"description": "",
"carpetarea": 0.0000,
"builduparea": 0.0000,
"spaceunit": "",
"availability": "",
"furnishingstatus": "",
"addressline1": "",
"addressline2": "",
"statecode": "",
"zipcode": null,
"roomtype": null,
"views": null,
"floor": null,
"ageofproperty": null,
"washroom": null,
"parkingavailable": null,
"reracertified": false,
"issold": false,
"direction": null,
"contactnumber": null,
"username": null,
"reranumber": null,
"name": null,
"number": null,
"negotiable": null
}
],
"propertyamenitiesdetails": [],
"propertyfacilitydetails": []
}

### Extraction Rules

1. **Allowed Field Values**

   * **listingtype**: "Buy", "Lease", "Pre-Leased"
   * **propertytype**: "Commercial Shop", "Office Space", "Showroom", "Warehouse"
   * **city**: "Thane", "Andheri", "Bandra", "Mulund", "Malad", "Mumbai"
   * **statecode**: "Maharashtra"
   * **spaceunit**: Always "Sq.Ft"
   * **availability**: "Under Construction" or "Ready To Move"
   * **furnishingstatus**: "None", "UnFurnished", "Furnished", "Semi Furnished"

2. **Numeric Fields**

   * `price`, `deposit`, `maintenance`, `carpetarea`, and `builduparea` must contain only numbers (no text, commas, or symbols).

3. **Area Extraction**

   * If the text mentions "Carpet", "Built-Up", "Super Built-Up", or "Area" followed by a number, capture it as `carpetarea` or `builduparea` respectively.  
   * If no unit is mentioned, assume `Sq.Ft` for `spaceunit`.

4. **Price and Negotiation Extraction**

   * If rent or price value includes text like "Negotiable", set `negotiable` to "Yes".  
   * Extract the numeric portion only for `price` (e.g., "68k" → 68000).  
   * If deposit mentions "month(s) rent", keep the numeric part in `deposit` as the equivalent number of months if explicit rent amount is given.

5. **Text Fields**

   * `ageofproperty`, `washroom`, and `parkingavailable` are free-text fields.  
     Examples: "3 years", "6 months", "2", "None", "Yes", etc.  
   * If text mentions "Parking", set `parkingavailable` to "Yes".

6. **Floor Details**

   * Capture text following the keyword "Floor" as `floor` (e.g., "2nd Floor", "Higher Lake Facing").

7. **Contact Extraction**

   * If a person’s name appears before or after a phone number, store it in the `name` field.  
     Example: "Anand Phalke 9969366661" → `"name": "Anand Phalke"`.  
   * Capture any 10-digit mobile number or number with country code as `"number"`.  
   * The same value can be assigned to `contactnumber` for consistency.

8. **Address Extraction**

   * Split full address into `addressline1`, `addressline2`, `city`, `statecode`, and `zipcode` (if available).  
   * Example:  
     "Location Hiranandani Estate Ghodbunder Road Thane West" →  
     `addressline1`: "Hiranandani Estate Ghodbunder Road",  
     `city`: "Thane".

9. **Description**

   * Provide a concise factual summary of the property’s main selling points (e.g., number of cabins, conference rooms, workstations, furnishing, parking).

10. **Amenities vs Facilities**

   * *Amenities* → On-site features (e.g., lift, parking, power backup).  
   * *Facilities* → Nearby conveniences (e.g., metro, schools, restaurants, banks).

11. **Booleans**

   * `reracertified` and `issold` must strictly be `true` or `false`.

12. **Default Values**

   * If `availability` is not explicitly mentioned, set it to `"Ready To Move"`.  
   * If `furnishingstatus` is not found but words like “Furnished” appear in the title or description, set it accordingly.  
   * If `furnishingstatus` is not mentioned anywhere, set it to `"None"`.  
   * If `statecode` is not mentioned, set it to `"Maharashtra"`.  
   * If `floor` is not mentioned, set it to `"Not Mentioned"`.  
   * If `washroom` is not mentioned, set it to `"Not Mentioned"`.  
   * If `parkingavailable` is not mentioned, set it to `"Not Mentioned"`.  
   * Keep all other fields as `null` unless explicitly found.

13. **Null Handling**

    * Use `null` when data is not available or not mentioned.

14. **Do Not Invent or Assume Data**

    * Only extract what is explicitly mentioned in the text (except for the default rules above).

15. **Output Format**

    * Return only valid structured JSON.
    * No commentary, extra text, or explanations outside the JSON object.

### Property Details
"""



@app.route('/extract', methods=['POST'])
def extract_property_details():
    try:
        data = request.get_json()
        property_text = data.get("propertyText")

        if not property_text:
            return jsonify({"error": "Missing 'propertyText' in request body"}), 400

        prompt = EXTRACTION_PROMPT + "\n\n" + property_text

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        raw_text = response.text.strip()

        # 🧹 Clean the Markdown fences (```json ... ```)
        cleaned = re.sub(r"^```json|```$", "", raw_text, flags=re.MULTILINE).strip()

        # 🧩 Try parsing JSON
        try:
            parsed_json = json.loads(cleaned)
            return jsonify(parsed_json)
        except json.JSONDecodeError:
            return jsonify({"rawText": raw_text, "error": "Invalid JSON format returned by model"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/')
def home():
    return jsonify({"message": "Real Estate Extraction API is running!"})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use Render's PORT or default to 5000 locally
    app.run(host="0.0.0.0", port=port, debug=True)
