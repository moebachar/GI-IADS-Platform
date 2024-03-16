from Importation import NamedBytesIO
import json
import base64


def read_json_and_convert_to_bytesio(json_file_path):
    # Read the JSON file
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)

    # Extract file names and base64 strings
    file_data_list = data.get("files", [])

    # Initialize an empty list to store (filename, BytesIO) tuples
    result = []

    for file_data in file_data_list:
        # Extract filename and base64 string from the dictionary
        filename = file_data.get("filename", "")
        base64_string = file_data.get("content", "")

        # Decode base64 string to get binary data
        binary_data = base64.b64decode(base64_string)

        # Create BytesIO object from binary data
        bytesio = NamedBytesIO(binary_data, filename)

        # Append (filename, BytesIO) tuple to the list
        result.append(bytesio)

    return result
