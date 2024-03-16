import os
import shutil
from Importation import NamedBytesIO
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision.transforms import ToTensor
import zipfile


class CustomDataset(Dataset):
    """
    Custom PyTorch dataset for loading paired image and label data.

    Args:
    - data: List of paired image and label data.

    Methods:
    - __len__(): Returns the total number of samples in the dataset.
    - __getitem__(idx): Returns the image and label at the specified index.
    """

    def __init__(self, data):
        """Returns the total number of samples in the dataset."""
        self.data = data
        self.transform = ToTensor()

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        """Returns the image and label at the specified index."""
        image, label = self.data[idx]
        image = self.transform(image)
        return image, label


class Exporter:
    """
    Class for exporting paired image and label data to a local directory.

    Args:
    - paired_files: List of paired image and label files.
    - split_parameters: Tuple containing train, validation, and test split percentages.

    Methods:
    - split_data(): Splits the paired data into training, validation, and test sets.
    - export_local(train_data, val_data, test_data): Exports the data to a local directory.
    - default_handling(): Performs the default handling of data export.
    """

    def __init__(self, paired_files, split_parameters=(0.8, 0.1, 0.1)):
        self.paired_files = paired_files
        self.split_parameters = split_parameters
        self.train_original = 0
        self.train_augmented = 0
        self.val_original = 0
        self.val_augmented = 0
        self.test_original = 0
        self.test_augmented = 0
        print(split_parameters)

    def split_data(self):
        """
        Splits the paired data into training, validation, and test sets.

        Returns:
        - train_data: Subset of paired data for training.
        - val_data: Subset of paired data for validation.
        - test_data: Subset of paired data for testing.
        """

        train_percentage, val_percentage, test_percentage = self.split_parameters
        total_size = len(self.paired_files)
        train_size = int(train_percentage * total_size)
        val_size = int(val_percentage * total_size)
        test_size = total_size - train_size - val_size

        train_data, val_data, test_data = random_split(
            self.paired_files, [train_size, val_size, test_size]
        )

        return train_data, val_data, test_data

    def export_local(self, train_data, val_data, test_data):
        """
        Exports the data to a local directory.

        Args:
        - train_data: Subset of paired data for training.
        - val_data: Subset of paired data for validation.
        - test_data: Subset of paired data for testing.
        """

        DIRECTORY_PATH = "C:/Users/hp/od_backend/data"
        os.makedirs(DIRECTORY_PATH, exist_ok=True)

        os.makedirs(DIRECTORY_PATH + "/train", exist_ok=True)
        os.makedirs(DIRECTORY_PATH + "/val", exist_ok=True)
        os.makedirs(DIRECTORY_PATH + "/test", exist_ok=True)

        os.makedirs(DIRECTORY_PATH + "/train/images", exist_ok=True)
        os.makedirs(DIRECTORY_PATH + "/train/labels", exist_ok=True)

        os.makedirs(DIRECTORY_PATH + "/val/images", exist_ok=True)
        os.makedirs(DIRECTORY_PATH + "/val/labels", exist_ok=True)

        os.makedirs(DIRECTORY_PATH + "/test/images", exist_ok=True)
        os.makedirs(DIRECTORY_PATH + "/test/labels", exist_ok=True)

        for image_file, label_file in train_data:
            print(image_file.name, label_file.name)
            image_path = os.path.join(DIRECTORY_PATH + "/train/images", image_file.name)
            label_path = os.path.join(DIRECTORY_PATH + "/train/labels", label_file.name)

            if image_file.name[:3] == "aug":
                self.train_augmented += 1
            else:
                self.train_original += 1

            with open(image_path, "wb") as f1:
                f1.write(image_file.read())

            with open(label_path, "wb") as f2:
                f2.write(label_file.read())

        for image_file, label_file in val_data:
            image_path = os.path.join(DIRECTORY_PATH + "/val/images", image_file.name)
            label_path = os.path.join(DIRECTORY_PATH + "/val/labels", label_file.name)

            if image_file.name[:3] == "aug":
                self.val_augmented += 1
            else:
                self.val_original += 1

            with open(image_path, "wb") as f1:
                f1.write(image_file.read())

            with open(label_path, "wb") as f2:
                f2.write(label_file.read())

        for image_file, label_file in test_data:
            image_path = os.path.join(DIRECTORY_PATH + "/test/images", image_file.name)
            label_path = os.path.join(DIRECTORY_PATH + "/test/labels", label_file.name)

            if image_file.name[:3] == "aug":
                self.test_augmented += 1
            else:
                self.test_original += 1

            with open(image_path, "wb") as f1:
                f1.write(image_file.read())

            with open(label_path, "wb") as f2:
                f2.write(label_file.read())

    def zip_it(
        self,
        zip_path="C:/Users/hp/od_backend/data_zip.zip",
        folder_path="C:/Users/hp/od_backend/data",
    ):
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, folder_path))

    def default_handling(self):
        """Performs the default handling of data export."""
        train_data, val_data, test_data = self.split_data()

        self.export_local(train_data, val_data, test_data)
        self.zip_it()
