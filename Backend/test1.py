from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64
from augmentation import Augmenter
from Importation import FilesHandler, FileCsvHandler, NamedBytesIO
from image_trans import ImageTrans, ImageTransTensor
import os
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt

from exportaion import Exporter
from fake_client import read_json_and_convert_to_bytesio


def mimic_get_files_from_client(
    folder_path="C:/Users/hp/od_backend/input_data",
):
    byteios = []

    # List all files in the folder
    files = [
        f
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]

    for file_name in files:
        file_path = os.path.join(folder_path, file_name)

        # Read file contents as bytes
        with open(file_path, "rb") as file:
            file_content = file.read()

            # Create BytesIO object
            byteio = BytesIO(file_content)

            # Append BytesIO object to the list
            byteios.append({"byteio": byteio, "filename": file_name})
    files = [
        NamedBytesIO(file["byteio"].read(), name=file["filename"]) for file in byteios
    ]
    return files


def show_result_images(result):
    # client_files = mimic_get_files_from_client()  # request.files.getlist("files")
    # files = [
    #     NamedBytesIO(file["byteio"].read(), name=file["filename"])
    #     for file in client_files
    # ]
    # files_handler = FilesHandler(files)
    # result = files_handler.default_handling()
    image_list = []

    for i in range(result):
        image_list.append(result[i][0])

    num_images = len(image_list)
    cols = int(np.ceil(np.sqrt(num_images)))
    rows = int(np.ceil(num_images / cols))

    # Create a figure and axis
    fig, axes = plt.subplots(rows, cols, figsize=(10, 10))

    # Flatten the axes so that we can iterate over them easily
    axes = axes.flatten()

    # Iterate over the images and plot them
    for i, img in enumerate(image_list):
        axes[i].imshow(img, cmap="gray")  # Assuming the images are grayscale
        axes[i].axis("off")

    # Adjust layout to prevent clipping of subplots
    plt.tight_layout()

    # Show the plot
    plt.show()


def testExporter():
    client_files = read_json_and_convert_to_bytesio(
        "C:/Users/hp/flask-react/flask-server/client_post/post1.json"
    )  # mimic_get_files_from_client()  # request.files.getlist("files")
    files = [
        NamedBytesIO(file["byteio"].read(), name=file["filename"])
        for file in client_files
    ]
    files_handler = FilesHandler(files)
    result = files_handler.default_handling()

    exporter = Exporter(result)

    exporter.default_handling()
