import requests
import json

# Replace this URL with your Flask API endpoint
api_url = "http://127.0.0.1:5000/label_images"

# Replace this data with the payload you want to send
payload = {
    "image_ids": list(map(int, input("give two ids to label : ").strip().split()))
}

# Send a POST request to the API
response = requests.post(api_url, json=payload)

# Check the response
if response.status_code == 200:
    print("Success!")
    formatted_json = json.dumps(response.json(), indent=2)
    print("response : ")
    print(formatted_json)
else:
    print("Failed!")
    print("Status Code:", response.status_code)
    print("Response:", response.text)
