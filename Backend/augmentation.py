import cv2
import numpy as np
from image_trans import ImageTrans, NamedBytesIO
from datetime import datetime

from torchvision.transforms.v2 import (
    RandomVerticalFlip,
    RandomHorizontalFlip,
    RandomRotation,
    RandomCrop,
    RandomAffine,
    ColorJitter,
    GaussianBlur,
    Grayscale,
    Compose,
)
from torchvision.transforms import ToPILImage, ToTensor
from torchvision.tv_tensors import BoundingBoxes


class Augmenter:
    """
    Class for data augmentation on images and bounding boxes.

    Args:
    - image: BytesIO object containing image data.
    - label: BytesIO object containing label data.
    - augmentation_ids: List of indices representing augmentations to apply.
    - rotaion_degrees: Rotation degrees for RandomRotation.
    - crop_size: Size of the crop for RandomCrop.
    - shear: Shear range for RandomAffine.
    - shear_degress: Degrees for shear in RandomAffine.
    - hue: Range of hue adjustment for ColorJitter.
    - saturation: Range of saturation adjustment for ColorJitter.
    - brightness: Range of brightness adjustment for ColorJitter.
    - gaussian_blur_kernel_size: Kernel size for GaussianBlur.

    Methods:
    - augment(): Applies specified augmentations to the image and bounding boxes.
    - get_augmented_files(): Returns augmented image and label as NamedBytesIO objects.
    - get_annotated_image(): Returns annotated image with bounding boxes.
    """

    def __init__(self, image, label, options, classes):
        """
        Initializes the Augmenter object.

        Args:
        - image: BytesIO object containing image data.
        - label: BytesIO object containing label data.
        - augmentation_ids: List of indices representing augmentations to apply.
        - rotaion_degrees: Rotation degrees for RandomRotation.
        - crop_size: Size of the crop for RandomCrop.
        - shear: Shear range for RandomAffine.
        - shear_degress: Degrees for shear in RandomAffine.
        - hue: Range of hue adjustment for ColorJitter.
        - saturation: Range of saturation adjustment for ColorJitter.
        - brightness: Range of brightness adjustment for ColorJitter.
        - gaussian_blur_kernel_size: Kernel size for GaussianBlur.
        """

        augmenters = []

        for key, value in zip(options.keys(), options.values()):
            if key == "vertical_flip":
                augmenters.append(RandomVerticalFlip(p=1))
            if key == "horizontal_flip":
                augmenters.append(RandomHorizontalFlip(p=1))
            if key == "rotation":
                augmenters.append(RandomRotation(degrees=value["degrees"]))
            if key == "random_crop":
                augmenters.append(RandomCrop(size=value["crop_size"]))
            if key == "shear":
                augmenters.append(
                    RandomAffine(degrees=value["degrees"], shear=value["shear"])
                )
            if key == "grayscale":
                augmenters.append(Grayscale(num_output_channels=3))
            if key == "hue":
                augmenters.append(ColorJitter(hue=value["hue"]))
            if key == "saturation":
                augmenters.append(ColorJitter(saturation=value["saturation"]))
            if key == "brightness":
                augmenters.append(ColorJitter(brightness=value["brightness"]))
            if key == "blur":
                augmenters.append(GaussianBlur(kernel_size=value["kernel_size"]))

        self.image_name = image.name
        self.label_name = label.name
        image_trans = ImageTrans(image, label, classes)
        self.image, boxes = image_trans.get_image_boxes()
        self.classes = image_trans.get_image_classes()
        height, width, _ = self.image.shape
        self.boxes = BoundingBoxes(boxes, format="XYXY", canvas_size=(height, width))
        self.transform = Compose(augmenters)

    def _boxes_trans(self, x_min, y_min, x_max, y_max, width, height):
        x_center = (x_min + x_max) / (2.0 * width)
        y_center = (y_min + y_max) / (2.0 * height)
        box_width = (x_max - x_min) / width
        box_height = (y_max - y_min) / height
        return x_center, y_center, box_width, box_height

    def augment(self):
        """
        Applies specified augmentations to the image and bounding boxes.

        Returns:
        - image: Augmented image.
        - boxes: Augmented bounding boxes.
        """

        to_pil_image = ToPILImage()
        to_tensor = ToTensor()
        img = to_tensor(self.image)
        image, boxes = self.transform(img, self.boxes)

        image = np.array(to_pil_image(image))
        boxes = boxes.numpy()
        return image, boxes

    def get_augmented_files(self):
        """
        Returns augmented image and label as NamedBytesIO objects.

        Returns:
        - image: Augmented image as NamedBytesIO.
        - bytes_io: Augmented label as NamedBytesIO.
        """

        image, boxes = self.augment()
        height, width, _ = image.shape

        # Get the current date and time
        current_date_time = datetime.now()
        date_string = current_date_time.strftime("%Y-%m-%d-%H-%M-%S")
        _, buffer = cv2.imencode(f".png", cv2.cvtColor(image, cv2.COLOR_BGR2RGBA))
        image = NamedBytesIO(buffer.tobytes(), "aug" + date_string + self.image_name)

        result_string = ""

        for class_index, row in zip(self.classes, boxes):
            new_row = self._boxes_trans(*row, width, height)
            # Convert each element to a string and join them with spaces
            row_string = str(class_index) + " " + " ".join(map(str, new_row))

            # Append the row string with a newline character to the result string
            result_string += row_string + "\n"

        # Format the date as a string

        bytes_io = NamedBytesIO(
            result_string.encode(), "aug" + date_string + self.label_name
        )

        return image, bytes_io

    def get_annotated_image(self):
        """
        Returns annotated image with bounding boxes.

        Returns:
        - result: NamedBytesIO object containing the annotated image.
        """

        image, boxes = self.augment()

        for x_min, y_min, x_max, y_max in boxes:
            image = cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

        _, buffer = cv2.imencode(f".png", cv2.cvtColor(image, cv2.COLOR_BGR2RGBA))

        return NamedBytesIO(buffer.tobytes())
