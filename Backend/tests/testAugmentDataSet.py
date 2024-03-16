import requests
import json

# Replace this URL with your Flask API endpoint
api_url = "http://127.0.0.1:5000/augment_dataSet"

possible_options = {
    "vertical_flip": None,
    "horizontal_flip": None,
    "rotation": {"degrees": 50},
    "random_crop": {"crop_size": 300},
    "shear": {"degrees": 1, "shear": (-15, 15, -15, 15)},
    "grayscale": None,
    "hue": {"hue": (-0.1, 0.1)},
    "saturation": {"saturation": (0, 3)},
    "brightness": {"brightness": (0, 3)},
    "blur": {"kernel_size": 15},
}


# Replace this data with the payload you want to send
payload = {
    "dataset_id": input("dataset_id : "),
    "pipelines": [
        {key: value}
        for key, value in zip(possible_options.keys(), possible_options.values())
    ],
}

print(payload)


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
