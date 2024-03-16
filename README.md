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

## Screenshots
Include a screenshot for each step of the process with a description.

## Contributing
Provide guidelines for contributing to your project. Include information on how users can report issues or submit pull requests.

## License
Specify the license under which your project is distributed.
