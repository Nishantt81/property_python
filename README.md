🏠 Real Estate Data Extraction API

A Flask-based REST API that uses Google Gemini (GenAI) to extract structured real estate information (like price, area, location, and amenities) from unstructured property text.

This API accepts free-form text descriptions and returns clean, standardized JSON suitable for property listing applications or data pipelines.

🚀 Features

Extracts structured property data from plain text using AI

Powered by Google Gemini 2.5 Flash model

Enforces a strict JSON schema for consistent data output

Handles invalid or malformed JSON gracefully

Includes CORS support for frontend integration

Ready for deployment on Render, Railway, Vercel, or any cloud platform

🧰 Tech Stack

Python 3.10+

Flask

Flask-CORS

Google GenAI SDK (google-genai)

dotenv for environment management

📦 Installation
1. Clone the repository
git clone https://github.com/Nishantt81/property_python.git
cd real-estate-extraction-api

2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows

3. Install dependencies
pip install -r requirements.txt

4. Configure environment variables

Create a .env file in the root directory and add:

GOOGLE_API_KEY=your_google_genai_api_key_here
PORT=5000

▶️ Running the Server
python app.py


Server will start at:

http://0.0.0.0:5000


Test root endpoint:

GET http://localhost:5000/


Response:

{
  "message": "Real Estate Extraction API is running!"
}

🔍 API Usage
Endpoint: /extract

Method: POST

Request Body:

{
  "propertyText": "Office space for rent in Hiranandani Estate Thane West. 500 sq.ft carpet, 1 washroom, fully furnished, rent 68k, deposit 2 months, contact Anand 9969366661."
}


Response Example:

{
  "propertyDetails": [
    {
      "propertytype": "Office Space",
      "listingtype": "Lease",
      "title": "Office space for rent in Hiranandani Estate Thane West",
      "price": 68000,
      "deposit": 136000,
      "maintenance": 0,
      "location": "Hiranandani Estate Thane West",
      "city": "Thane",
      "description": "Fully furnished office with 1 washroom.",
      "carpetarea": 500,
      "builduparea": null,
      "spaceunit": "Sq.Ft",
      "availability": "Ready To Move",
      "furnishingstatus": "Furnished",
      "addressline1": "Hiranandani Estate Thane West",
      "statecode": "Maharashtra",
      "zipcode": null,
      "washroom": "1",
      "parkingavailable": "Not Mentioned",
      "reracertified": false,
      "issold": false,
      "contactnumber": "9969366661",
      "name": "Anand",
      "negotiable": null
    }
  ],
  "propertyamenitiesdetails": [],
  "propertyfacilitydetails": []
}


If the model returns invalid JSON:

{
  "rawText": "<model output>",
  "error": "Invalid JSON format returned by model"
}

⚙️ Environment Variables
Variable	Description	Example
GOOGLE_API_KEY	Google GenAI API Key	AIza...
PORT	Port for Flask server	5000
🧱 Project Structure
real-estate-extraction-api/
│
├── app.py                # Main Flask app
├── .env                  # Environment variables
├── requirements.txt      # Dependencies
└── README.md             # Documentation

🧩 Example Frontend Integration (JavaScript)
fetch("http://localhost:5000/extract", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    propertyText: "Shop for sale in Bandra West, 300 sq.ft built-up area, price 1.5 Cr."
  })
})
  .then(res => res.json())
  .then(data => console.log(data))
  .catch(err => console.error(err));

☁️ Deployment

You can deploy this API easily on:

Render

Railway

Google Cloud Run

Vercel

Make sure to:

Set your environment variables in the platform’s dashboard

Use host 0.0.0.0 and port $PORT

📜 License

MIT License © 2025
Feel free to use, modify, and distribute this project.

✅ Maintained by Nishant
