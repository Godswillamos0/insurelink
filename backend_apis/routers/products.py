import requests
import json

url = "https://api.playbox.grow.curacel.co/api/v1/products"

headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer 2825|nUiD3cPL6p1pTb9acrQRHmrvKao1cLrGLDPkonta784e8389'
}

response = requests.get(url, headers=headers)

def extract_important_insurance_details():
    parsed_json = response.json()

    extracted_data = []

    for item in parsed_json.get("data", []):
        title = item.get("title")
        insurer = item.get("insurer", {})
        product_type = item.get("product_type", {})

        detail = {
            "title": title,
            "insurer_name": insurer.get("name"),
            "insurer_logo": insurer.get("logo_url"),
            "product_type": product_type.get("name"),
            "product_icon": product_type.get("icon_url"),
            "price": item.get("price"),
            "price_unit": item.get("premium_rate_unit"),
            "frequency": item.get("premium_frequencies", []),
        }

        extracted_data.append(detail)

    return json.dumps(extracted_data, indent=2)
