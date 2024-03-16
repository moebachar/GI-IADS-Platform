import base64
from PIL import Image
import cv2
import numpy as np
from io import BytesIO
from Importation import NamedBytesIO
from torchvision.transforms import v2
from torchvision import tv_tensors
from PIL import Image
import matplotlib.pyplot as plt
from math import ceil, sqrt
import hashlib


def hash_word_to_color(word):
    # Use SHA-256 hash function to generate a hash
    hash_value = hashlib.sha256(word.encode()).hexdigest()

    # Take the first 6 characters of the hash as the color code
    color_code = hash_value[:6]

    # Convert the hex color code to RGB values
    r = int(color_code[:2], 16)
    g = int(color_code[2:4], 16)
    b = int(color_code[4:], 16)

    return (r, g, b)


class ImageTrans:

    """
    Class for transforming and annotating images with bounding boxes.

    Args:
    - image_bytesio: BytesIO object containing image data.
    - text_bytesio: BytesIO object containing text data.

    Methods:s
    - get_image_boxes(): Extracts image and bounding box information.
    - bounding_box(): Draws bounding boxes on the image.
    - show(): Displays the image with bounding boxes using OpenCV.
    - get_annotated_image(): Returns an annotated image with bounding boxes.
    """

    def __init__(self, image_bytesio, text_bytesio, classes):
        self.image = image_bytesio
        self.text = text_bytesio
        self.classes = classes.strip().split("\r\n")
        self.colors = list(map(hash_word_to_color, classes))

    def get_image_boxes(self) -> tuple:
        """
        Extracts image and bounding box information from input data.

        Returns:
        - image: NumPy array representing the image.
        - boxes: List of tuples representing bounding box coordinates.
        """

        image = np.array(Image.open(self.image))
        lines = self.text.getvalue().decode().splitlines()
        height, width, _ = image.shape
        boxes = []
        for line in lines:
            values = line.strip().split(" ")
            x_center, y_center, box_width, box_height = map(float, values[1:])

            x_min = int((x_center - box_width / 2) * width)
            y_min = int((y_center - box_height / 2) * height)
            x_max = int((x_center + box_width / 2) * width)
            y_max = int((y_center + box_height / 2) * height)
            boxes.append((x_min, y_min, x_max, y_max))
        return image, boxes

    def get_image_classes(self) -> list:
        """
        Extracts classes from input data.

        Returns:
        - classes: array of classes index.
        """
        lines = self.text.getvalue().decode().splitlines()
        classes_indecies = []
        for line in lines:
            values = line.strip().split(" ")
            classes_indecies.append(int(values[0]))
        return classes_indecies

    def bounding_box(self):
        """
        Draws bounding boxes on the image.

        Returns:
        - image: NumPy array representing the image with bounding boxes.
        """

        image, boxes = self.get_image_boxes()
        classes_indecies = self.get_image_classes()
        for i, (x_min, y_min, x_max, y_max) in zip(classes_indecies, boxes):
            # Write text on the image
            text = self.classes[i]
            color = self.colors[i]
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            font_thickness = 2
            text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
            text_x = int(x_min + (x_max - x_min - text_size[0]) / 2)
            text_y = int(
                y_min - 10
            )  # Adjust the vertical position based on your requirements

            cv2.putText(
                image, text, (text_x, text_y), font, font_scale, color, font_thickness
            )

            image = cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, 2)
        return image

    def show(self):
        """Displays the image with bounding boxes using OpenCV."""

        image = self.bounding_box()
        cv2.imshow("Image with Bounding Boxes", cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def get_annotated_image(self):
        """
        Returns an annotated image with bounding boxes.

        Returns:
        - result: NamedBytesIO object containing the annotated image.
        """

        image = self.bounding_box()
        _, buffer = cv2.imencode(f".png", cv2.cvtColor(image, cv2.COLOR_BGR2RGBA))

        # Create a BytesIO object and write the encoded frame to it
        result = base64.b64encode(buffer).decode("utf-8")
        return result


class ImageShow:
    """
    Class for displaying a grid of images.

    Args:
    - images: List of image data (file paths or BytesIO objects).

    Methods:
    - show(): Displays a grid of images using Matplotlib.
    """

    def __init__(self, images):
        self.images = images
        self.n = ceil(sqrt(len(images)))

    def show(self):
        """Displays a grid of images using Matplotlib."""

        rows = self.n
        cols = self.n
        num_images = len(self.images)
        if num_images == 0:
            return

        fig = plt.figure(figsize=(10, 10))

        for i in range(num_images):
            image_data = self.images[i]
            image = Image.open(image_data)
            ax = fig.add_subplot(rows, cols, i + 1)
            # x_batch[i]: Image object at each iteration
            ax.imshow(image)

        plt.show()


class ImageTransTensor:
    def __init__(self, image_bytesio, text_bytesio):
        image_trans = ImageTrans(image_bytesio, text_bytesio)
        image, boxes = image_trans.get_image_boxes()

        transforms = v2.Compose(
            [
                v2.RandomResizedCrop(size=(224, 224), antialias=True),
                v2.RandomHorizontalFlip(p=1),
            ]
        )
        boxes = np.array(boxes)

        height, width, _ = image.shape
        boxes = tv_tensors.BoundingBoxes(
            boxes, format="XYXY", canvas_size=(height, width)
        )

        self.image, self.boxes = transforms(image, boxes)

    def get_annotated_image(self):
        image = self.image
        boxes = self.boxes.numpy()
        for x_min, y_min, x_max, y_max in boxes:
            image = cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

        _, buffer = cv2.imencode(f".png", cv2.cvtColor(image, cv2.COLOR_BGR2RGBA))

        # Create a BytesIO object and write the encoded frame to it
        result = NamedBytesIO(buffer.tobytes())

        return result
