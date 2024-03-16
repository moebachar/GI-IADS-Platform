from flask import Flask, request, jsonify, send_file
import cv2
import numpy as np
import base64
from Importation import FilesHandler, FileCsvHandler, NamedBytesIO
from image_trans import ImageTrans
from augmentation import Augmenter
from exportaion import Exporter
from database import *
import json
from test1 import mimic_get_files_from_client
import traceback
import os


def treat_image(image):
    _, buffer = cv2.imencode(f".png", cv2.cvtColor(image, cv2.COLOR_BGR2RGBA))

    # Create a BytesIO object and write the encoded frame to it
    return NamedBytesIO(buffer.tobytes())


def encode_image_to_base64(image_np):
    # Convert the NumPy array to image format (BGR)
    _, buffer = cv2.imencode(".jpg", image_np)

    # Encode the binary data to base64
    base64_encoded_image = base64.b64encode(buffer).decode("utf-8")

    return base64_encoded_image


app = Flask(__name__)


@app.route("/create_dataSet", methods=["POST"])
def create_dataSet():
    try:
        data = request.form
        name = data["name"]
        classes = data["classes"]
        create_dataset(name, classes)
        response = {"status": "success", "message": f"data set {name} created"}
        return jsonify(response), 200

    except Exception as e:
        # Handle exceptions or errors
        response = {"status": "error", "message": traceback.format_exc()}
        return jsonify(response), 500


@app.route("/delete_dataSet", methods=["POST"])
def delete_dataSet():
    try:
        # Get the JSON data from the request body
        data = request.form

        dataset_id = data["dataset_id"]
        delete_dataset(dataset_id)
        response = {"status": "success", "message": "data set deleted"}
        return jsonify(response), 200

    except Exception as e:
        # Handle exceptions or errors
        response = {"status": "error", "message": traceback.format_exc()}
        return jsonify(response), 500


@app.route("/merge_dataSets", methods=["POST"])
def merge_dataSets():
    try:
        # Get the JSON data from the request body
        data = request.form
        dataset_id1 = data["dataset_id1"]
        dataset_id2 = data["dataset_id2"]
        dataset_name = data["dataset_name"]
        merge_datasets(dataset_id1, dataset_id2, dataset_name)
        response = {"status": "success", "message": "data sets merged"}
        return jsonify(response), 200

    except Exception as e:
        # Handle exceptions or errors
        response = {"status": "error", "message": traceback.format_exc()}
        return jsonify(response), 500


@app.route("/dataSet_info", methods=["GET", "POST"])
def dataSet_info():
    try:
        # Get the JSON data from the request body
        data = request.form
        dataset_id = data["dataset_id"]

        info = dataset_info(dataset_id)
        response = {"status": "success", "info": info}
        return jsonify(response), 200

    except Exception as e:
        # Handle exceptions or errors
        response = {"status": "error", "message": traceback.format_exc()}
        return jsonify(response), 500


@app.route("/add_data_toDataSet", methods=["POST"])
def add_data_toDataSet():
    if "files" not in request.files:
        return jsonify({"error": "No files part"}), 500
    try:
        client_files = request.files.getlist("files")
        files = [NamedBytesIO(file.read(), name=file.filename) for file in client_files]
        files_handler = FilesHandler(files)
        result = files_handler.default_handling()

        data = request.form

        dataset_id = data["dataset_id"]

        for image, label in result:
            insert_image_and_label(image, label, dataset_id, False)
        empty_label = NamedBytesIO(name="empty.txt")

        for image in files_handler.non_labeled_images:
            insert_image_and_label(image, empty_label, dataset_id, False)

        response = {
            "status": "success",
            "message": "POST request successful",
            "fails": files_handler.fails,
        }

        return jsonify(response), 200

    except Exception as e:
        # Handle exceptions or errors
        response = {"status": "error", "message": traceback.format_exc()}
        return jsonify(response), 500


@app.route("/add_data_toDataSet_csv", methods=["POST"])
def add_data_toDataSet_csv():
    try:
        client_file = request.files.getlist("files")[0]
        files_handler = FileCsvHandler(client_file)
        result = files_handler.default_handling()

        data = request.form

        dataset_id = data["dataset_id"]

        for image, label in result:
            insert_image_and_label(image, label, dataset_id, False)
        empty_label = NamedBytesIO(name="empty.txt")

        for image in files_handler.non_labeled_images:
            insert_image_and_label(image, empty_label, dataset_id, False)

        response = {
            "status": "success",
            "message": "POST request successful",
            "fails": files_handler.fails,
        }

        return jsonify(response), 200

    except Exception as e:
        # Handle exceptions or errors
        response = {"status": "error", "message": traceback.format_exc()}
        return jsonify(response), 500


@app.route("/delete_images", methods=["POST"])
def delete_images():
    try:
        # Get the JSON data from the request body
        data = request.form
        image_ids = list(map(int, data["image_ids"].strip().split(",")))

        for image_id in image_ids:
            delete_image_and_label(image_id)

        response = {"status": "success", "message": "images deleted"}
        return jsonify(response), 200

    except Exception as e:
        # Handle exceptions or errors
        response = {"status": "error", "message": traceback.format_exc()}
        return jsonify(response), 500


@app.route("/label_images", methods=["POST"])
def label_images():
    try:
        newLabels = mimic_get_files_from_client("C:/Users/hp/od_backend/annotaions")
        data = request.get_json()
        image_ids = data.get(image_ids)

        for image_id, label in zip(image_ids, newLabels):
            add_label(label, image_id)
        response = {"status": "success", "message": "images labeled"}
        return jsonify(response), 200

    except Exception as e:
        # Handle exceptions or errors
        response = {"status": "error", "message": traceback.format_exc()}
        return jsonify(response), 500


@app.route("/get_dataSet", methods=["GET", "POST"])
def get_dataSet():
    try:
        # Get the JSON data from the request body
        data = request.form
        dataset_id = data["dataset_id"]
        image_label_pairs, non_labeled_images = get_dataset(dataset_id)
        classes = dataset_info(dataset_id)["classes"]

        labeled = []
        non_labeled = []
        for id, (image_file, label_file) in image_label_pairs:
            image_trans = ImageTrans(image_file, label_file, classes)
            labeled.append((id, image_trans.get_annotated_image()))

        for id, image_file in non_labeled_images:
            non_labeled.append(
                (id, base64.b64encode(image_file.read()).decode("utf-8"))
            )

        response = {
            "status": "success",
            "labeled": labeled,
            "non_labeled": non_labeled,
        }
        return jsonify(response), 200

    except Exception as e:
        # Handle exceptions or errors
        response = {"status": "error", "message": traceback.format_exc()}
        return jsonify(response), 500


@app.route("/get_dataSets", methods=["GET"])
def get_dataSets():
    try:
        datasets = get_all_datasets()
        response = {"status": "success", "data": datasets}
        return jsonify(response), 200

    except Exception as e:
        # Handle exceptions or errors
        response = {"status": "error", "message": traceback.format_exc()}
        return jsonify(response), 500


@app.route("/augment_dataSet", methods=["POST"])
def augment_dataSet():
    try:
        data = request.form
        dataset_id = data.get("dataset_id")
        pipelines = list(json.loads(data.get("pipelines")).values())[1:]
        image_label_pairs, _ = get_dataset(dataset_id)
        info = dataset_info(dataset_id)
        id = create_dataset(f"{info['name']} (augmented)", info["classes"])
        for options in pipelines:
            for _, (image, label) in image_label_pairs:
                augmenter = Augmenter(image, label, options, info["classes"])

                img, lbl = augmenter.get_augmented_files()
                insert_image_and_label(img, lbl, id, True)

        response = {
            "status": "success",
            "message": "data augmented in a new dataset",
            "piplines": pipelines,
        }
        return jsonify(response), 200

    except Exception as e:
        # Handle exceptions or errors
        response = {"status": "error", "message": traceback.format_exc()}
        return jsonify(response), 500


@app.route("/preview_augmentation", methods=["GET", "POST"])
def preview_augmentation():
    try:
        # Get the JSON data from the request body
        options = {}

        for key, value in request.form.items():
            options[key] = json.loads(value)

        image = None
        label = None
        with open("C:/Users/hp/od_backend/preview/test.jpg", "rb") as file:
            file_content = file.read()
            image = NamedBytesIO(file_content, file.name)

        with open("C:/Users/hp/od_backend/preview/test.txt", "rb") as file:
            file_content = file.read()
            label = NamedBytesIO(file_content, file.name)

        augmenter = Augmenter(image, label, options, "dog")
        image_file, label_file = augmenter.get_augmented_files()
        image_trans = ImageTrans(image_file, label_file, "dog")

        response = {"status": "success", "result": image_trans.get_annotated_image()}
        return jsonify(response), 200

    except Exception as e:
        # Handle exceptions or errors
        response = {"status": "error", "message": traceback.format_exc()}
        return jsonify(response), 500


@app.route("/export_dataSet", methods=["GET", "POST"])
def export_dataSet():
    try:
        # Get the JSON data from the request body
        data = request.form
        dataset_id = data["dataset_id"]
        split_parameters = (
            float(data["train"]),
            float(data["test"]),
            float(data["val"]),
        )
        print(split_parameters)
        image_label_pairs, _ = get_dataset(dataset_id)

        exporter = Exporter(
            [(image, label) for (id, (image, label)) in image_label_pairs],
            split_parameters=split_parameters,
        )
        exporter.default_handling()
        zip_file_path = "C:/Users/hp/od_backend/data_zip.zip"

        # Check if the zip file exists
        if os.path.exists(zip_file_path):
            # Send the zip file as a response
            return send_file(zip_file_path, as_attachment=True)
        else:
            # Handle the case where the zip file does not exist
            return "Zip file not found", 404

    except Exception as e:
        # Handle exceptions or errors
        response = {"status": "error", "message": traceback.format_exc()}
        return jsonify(response), 500


if __name__ == "__main__":
    app.run(debug=True)
