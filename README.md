# Automated Object Detection Platform

## Overview
Introducing the Object Detection App, a tool designed for efficient object detection workflows. Users can easily import both local and external data in various formats, ensuring compatibility with diverse datasets. The app's advanced cleaning features help maintain dataset accuracy, while its intuitive labeling system facilitates precise object categorization. With built-in preprocessing options like data splitting and augmentation, the Object Detection App optimizes datasets for improved model training. The app also generates detailed reports on data quality, providing valuable insights for users. With a user-friendly interface, the Object Detection App simplifies the object detection process, making it an essential tool for streamlined data management.

![Platform Overview](https://github.com/moebachar/GI-IADS-Platform/blob/main/images/1.png)

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Frontend (ReactJS)

For the frontend, you can use npm to install the dependencies. Ensure you have Node.js and npm installed.

```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install
```

### Backend (Flask)

For the backend, you'll need to set up a virtual environment, install the dependencies, and then run the Flask server.

#### Unix-Based Systems (Linux, macOS)

```bash
# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Navigate to the backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Install dependencies
pip install flask python-dotenv

# Run the Flask server
python server.py
```

#### Windows

```bash
# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate

# Navigate to the backend directory
cd backend

# Install dependencies
pip install flask python-dotenv

# Run the Flask server
python server.py
```

Make sure to replace `frontend` and `backend` with the actual directories containing your frontend and backend code. Also, ensure that your `requirements.txt` file in the backend directory contains all the necessary dependencies for your Flask application.

These instructions should guide users through setting up both the frontend and backend components of your automated object detection platform, accommodating different operating systems.

## Usage
### Step 1: Click on Object Detection

![Step 1: Click on Object Detection](https://github.com/moebachar/GI-IADS-Platform/raw/main/images/2.png)

Click on the "Object Detection" button to start the detection process. This button is typically located in the main navigation menu or toolbar of the platform's user interface.

### Step 2: Open the Data Set Creation Modal

![Step 2: Open the Data Set Creation Modal](https://github.com/moebachar/GI-IADS-Platform/raw/main/images/3.png)

Click on the plus button or any other relevant action to open the modal for creating a new data set. This action typically triggers a modal or a dialog box to appear on the screen, where you can input details for the new data set.

### Step 3: Add Images and Labels to the Data Set

![Step 3: Add Images and Labels to the Data Set](https://github.com/moebachar/GI-IADS-Platform/raw/main/images/4.png)

Once the data set is created, it will be empty. To populate it with images and labels (optional), you can either click on the "Add Data Now" button or head to the "Importation" section. Clicking the "Add Data Now" button usually opens a file uploader interface where you can select and upload images along with optional labels. Alternatively, in the "Importation" section, you may find more advanced options for importing data sets from external sources or files.

### Step 4: Import Images and Corresponding Labels

![Step 4: Import Images and Corresponding Labels](https://github.com/moebachar/GI-IADS-Platform/raw/main/images/5.png)

To import images along with their corresponding labels, ensure they have the same name. Images without corresponding labels will still be uploaded and can be labeled later within the platform. After importing the images, click on the plus button located at the bottom right corner. From the options that appear, select the dataset to which you want to add the images.

### Step 5: View the Data Set

![Step 5: View the Data Set](https://github.com/moebachar/GI-IADS-Platform/raw/main/images/6.png)

To view the dataset, navigate to the "Data Sets" section from the main navigation menu. From the list of datasets, select the corresponding dataset that you want to view. This will display the dataset details, including the imported images and any associated labels. You can now proceed with preprocessing or further analysis of the dataset.

### Step 6: Annotate Images

![Step 6: Annotate Images](https://github.com/moebachar/GI-IADS-Platform/raw/main/images/7.png)

Head to the "Label" section from the main navigation menu. Select a dataset with non-labeled images. Start annotating by simply dragging and dropping bounding boxes or annotations onto the images. You can freely navigate through all unlabeled images in the dataset, providing annotations as necessary. This process allows you to label and annotate images for training or further analysis.

### Step 7: Create Augmented Dataset

![Step 7: Create Augmented Dataset](https://github.com/moebachar/GI-IADS-Platform/raw/main/images/8.png)

Navigate to the "Augmentation" section from the main navigation menu. Begin by creating a pipeline of augmentation techniques by clicking on the plus blue button at the end of the pipeline. This action allows you to add various augmentation techniques such as rotation, scaling, or flipping to the pipeline. Once the pipeline is set up, apply it to the dataset to generate an augmented version suitable for training or analysis.

### Step 8: Customize Augmentation Techniques

![Step 8: Customize Augmentation Techniques](https://github.com/moebachar/GI-IADS-Platform/raw/main/images/9.png)

In the "Augmentation" section, after creating a pipeline of augmentation techniques, you can customize each technique by clicking on the settings icon next to it. This action will reveal a slider with corresponding parameters that you can adjust according to your preferences. Fine-tune parameters such as rotation angle, scaling factor, or flipping probability to tailor the augmentation to your dataset's specific requirements.

### Step 9: Validate Pipelines and Generate New Dataset

![Step 9: Validate Pipelines and Generate New Dataset](https://github.com/moebachar/GI-IADS-Platform/raw/main/images/10.png)

After configuring each augmentation pipeline, preview its results to ensure the desired transformations are applied correctly. Click on the "Validate" button on the screen to validate the pipeline. Once validated, you can add multiple other pipelines as needed.

To generate a new dataset, the images in the dataset will be processed simultaneously in each pipeline. Click on the button located at the bottom right corner to initiate the generation process. The size of the new dataset will be calculated as:

\[
\text{{size}}_{\text{{new dataset}}} = \text{{number\_of\_pipelines}} \times \text{{number\_of\_images}}
\]

### Step 10: Merge Datasets

![Step 10: Merge Datasets](https://github.com/moebachar/GI-IADS-Platform/raw/main/images/11.png)

Navigate to the "Merge" section from the main navigation menu. Here, you can merge two datasets, such as the original dataset with its augmented version or any other combinations.

Choose the datasets you want to merge and decide whether to delete the original datasets after merging or not. This option allows you to manage your storage efficiently while creating a unified dataset for further analysis or training.

### Step 11: Export Dataset

![Step 11: Export Dataset](https://github.com/moebachar/GI-IADS-Platform/raw/main/images/12.png)

Navigate to the "Exportation" section from the main navigation menu. Here, you can export the dataset to your local machine or directly to model training.

Choose the export destination by clicking on one of the buttons at the bottom. You can also specify the splitting parameters for dividing the dataset into training, testing, and validation sets.

The exported dataset will be packaged as a zip file with the following structure:

data set name

-> train
  --> images
  --> labels

-> test
  --> images
  --> labels

-> val
  --> images
  --> labels


This structured zip file allows for easy integration with various machine learning frameworks and tools for training models.


## Documentation

For detailed documentation and user guides, please refer to the [platform documentation](https://documentation-platform-hosting.readthedocs.io/en/latest/Detection/Data%20Processing/user.html). The documentation provides comprehensive instructions on using various features of the platform, including data processing, object detection, and more.

