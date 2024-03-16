import os
import pandas as pd
from io import BytesIO
import requests


class NamedBytesIO(BytesIO):

    """
    A subclass of BytesIO with an additional 'name' attribute.

    Attributes:
        name (str): The name associated with the BytesIO object.
    """

    def __init__(self, initial_bytes=b"", name=None):
        """
        Initializes a NamedBytesIO object.

        Args:
            initial_bytes (bytes): Initial bytes for the BytesIO.
            name (str): The name associated with the BytesIO object.
        """
        super().__init__(initial_bytes)
        self.name = name


class FilesHandler:
    """
    Handles a collection of files, separating them by type and performing default handling.

    Attributes:
        files (list): List of file-like objects to be processed.
        image_types (list): List of allowed image file extensions.
        label_types (list): List of allowed label file extensions.
        fails (list): List to store files that failed processing.
    """

    def __init__(self, files, image_types=None, label_types=None):
        """
        Initializes a FilesHandler object.

        Args:
            files (list): List of file-like objects to be processed.
            image_types (list, optional): List of allowed image file extensions.
            label_types (list, optional): List of allowed label file extensions.
        """

        self.files = files
        self.image_types = image_types or ["png", "jpg", "jpeg"]
        self.label_types = label_types or ["txt", "yaml"]
        self.fails = {"empty": [], "unmatched": [], "other": []}
        self.non_labeled_images = []

    def _get_extension(self, file_name) -> str:
        """
        Extracts the file extension from a given file name.

        Args:
            file_name (str): The name of the file.

        Returns:
            str: The file extension in lowercase.
        """

        # Split the file name into base name and extension
        base_name, extension = file_name.rsplit(".", 1)

        # Return the extension (in lowercase to handle cases like 'TXT' or 'Txt')
        return extension.lower()

    def separate_files_by_type(self) -> tuple:
        """
        Separates files into two lists based on their types: images and labels.

        Returns:
            tuple: A tuple containing two lists - images and labels.
        """

        images = []
        labels = []

        for file in self.files:
            file_type = self._get_extension(file.name)

            if file_type in self.image_types:
                images.append(file)
            elif file_type in self.label_types:
                labels.append(file)
            else:
                self.fails["other"].append(file.name)

        return images, labels

    def pair(self, images, labels) -> list:
        """
        Pairs image and label files based on their names.

        Args:
            images (list): List of image file-like objects.
            labels (list): List of label file-like objects.

        Updates:
            fails (list): Updated list of failed files.

        Returns:
            list: A list of tuples, each containing a paired image and label file.
        """

        paired_results = []
        matched_labels = []

        for image_file in images:
            image_name, _ = os.path.splitext(os.path.basename(image_file.name))

            corresponding_label = None
            for label_file in labels:
                label_name, _ = os.path.splitext(os.path.basename(label_file.name))

                if image_name == label_name:
                    corresponding_label = label_file
                    break

            if corresponding_label:
                paired_results.append((image_file, corresponding_label))
                matched_labels.append(corresponding_label)
            else:
                self.non_labeled_images.append(image_file)

        # Check for unmatched label files
        unmatched_labels = [
            label.name for label in labels if label not in matched_labels
        ]

        self.fails["unmatched"].extend(unmatched_labels)

        return paired_results

    def remove_empty(self) -> None:
        """
        Removes empty files from the list of files.

        Updates:
            files (list): Updated list of non-empty file-like objects.
            fails (list): Updated list of failed files.
        """
        non_empty_files = [file for file in self.files if file.getvalue()]
        empty_files = [file.name for file in self.files if file not in non_empty_files]

        self.fails["empty"].extend(empty_files)
        self.files = non_empty_files

    def default_handling(self) -> list:
        """
        Performs default handling of files:

        1. Removes empty files.
        2. Separates files by type (images and labels).
        3. Pairs images and labels based on names.

        Returns:
            list: A list of tuples, each containing a paired image and label file.
        """
        # Remove empty files
        self.remove_empty()

        # Separate files by type
        images, labels = self.separate_files_by_type()

        # Pair images and labels
        paired_results = self.pair(images, labels)

        return paired_results


class FileCsvHandler:
    """
    Handles CSV files containing image links and labels.

    Attributes:
        file (file-like object): The CSV file to be processed.
        image_links (list): List of image links extracted from the CSV.
        labels (list): List of labels extracted from the CSV.
        fails (list): List to store files that failed processing.
    """

    def __init__(self, file):
        """
        Initializes a FileCsvHandler object.

        Args:
            file (file-like object): The CSV file to be processed.
        """

        self.image_links = []
        self.labels = []
        self.fails = {"empty": [], "other": [], "unmatched": []}
        self.errors = self._process_csv(file)
        self.non_labeled_images = []

    def _process_csv(self, file) -> list:
        """
        Processes the CSV file to extract image links and labels.

        Args:
            file (file-like object): The CSV file to be processed.
        """
        errors = []
        try:
            # Read the CSV file using pandas
            df = pd.read_excel(BytesIO(file.read()))

            # Check if 'images' column exists
            if "images" in df.columns:
                self.image_links = list(df["images"])
            else:
                errors.append('"images" column unfound!')

            # Check if 'labels' column exists
            if "labels" in df.columns:
                # Convert the 'labels' column to a list of multiline strings
                self.labels = [
                    str(label) for label in df["labels"].str.replace("\\n", "\n")
                ]
            else:
                errors.append('"labels" column unfound!')

        except pd.errors.EmptyDataError:
            # Handle empty file
            errors.append("The given file is empty!")

        return errors

    def fetch_images(self) -> list:
        """
        Fetches images from the provided image links.

        Returns:
            list: A list of NamedBytesIO objects containing image data.
        """

        images = []
        for index, image_link in enumerate(self.image_links):
            try:
                response = requests.get(image_link)
                if response.status_code == 200:
                    image_bytes = response.content
                else:
                    image_bytes = b""
                    self.fails["other"] = image_link
            except requests.RequestException:
                image_bytes = b""
                self.fails["other"] = image_link

            # Create a NamedBytesIO object and append it to the local 'images' list
            images.append(
                NamedBytesIO(initial_bytes=image_bytes, name=str(index) + ".png")
            )

        return images

    def pair(self, images) -> list:
        """
        Pairs images with labels and handles empty labels.

        Args:
            images (list): List of image NamedBytesIO objects.

        Returns:
            list: A list of tuples, each containing a paired image and label NamedBytesIO.
        """

        pairs = []
        min_length = min(len(self.labels), len(images))

        for i in range(min_length):
            label_text = self.labels[i]
            if not label_text or label_text == "nan":
                # Pair with an empty NamedBytesIO text file if label is empty
                label_io = NamedBytesIO(name=str(i) + ".txt")
            else:
                # Pair with a NamedBytesIO text file read from the label text
                label_io = NamedBytesIO(
                    initial_bytes=label_text.encode("utf-8"), name=str(i) + ".txt"
                )

            image = images[i]
            pairs.append((image, label_io))
            if image.getvalue() and not label_io.getvalue():
                self.fails["unmatched"].append(image.name)
            if not image.getvalue() and label_io.getvalue():
                self.fails["unmatched"].append(label_io.name)

        # Pair the rest with empty NamedBytesIO text files
        for i in range(min_length, len(images)):
            pairs.append((images[i], NamedBytesIO(name=str(i) + ".txt")))

        return pairs

    def remove_empty(self, pairs) -> list:
        """
        Removes pairs with empty images or labels.

        Args:
            pairs (list): List of tuples containing paired image and label NamedBytesIO.

        Returns:
            list: A list of non-empty image and label pairs.
        """
        non_empty_pairs = []
        for image, label in pairs:
            if image.getvalue() and label.getvalue():
                non_empty_pairs.append((image, label))
            elif not label.getvalue():
                self.non_labeled_images.append(image)
        return non_empty_pairs

    def default_handling(self) -> list:
        """
        Performs default handling of the CSV file:

        1. Reads the CSV file and extracts image links and labels.
        2. Fetches images from the provided image links.
        3. Pairs images with labels.
        4. Removes pairs with empty images or labels.

        Returns:
            list: A list of non-empty tuples, each containing a paired image and label NamedBytesIO.
        """

        images = self.fetch_images()
        pairs = self.pair(images)
        non_empty_pairs = self.remove_empty(pairs)

        return non_empty_pairs
