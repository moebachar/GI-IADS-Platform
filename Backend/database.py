import sqlite3

from Importation import NamedBytesIO


def create_database():
    # Connect to SQLite database (or create it if it doesn't exist)
    connection = sqlite3.connect("OD.db")
    cursor = connection.cursor()

    # Create Label table
    cursor.execute(
        """
        CREATE TABLE Label (
            id_label INTEGER PRIMARY KEY AUTOINCREMENT,
            name_label TEXT,
            label BLOB,
            size_label REAL,
            augmented_label INTEGER
        )
    """
    )

    # Create Image table
    cursor.execute(
        """
        CREATE TABLE Image (
            id_image INTEGER PRIMARY KEY AUTOINCREMENT,
            name_image TEXT,
            image BLOB,
            size_image REAL,
            augmented_image INTEGER,
            id_label INTEGER,
            id_dataSet INTEGER,
            FOREIGN KEY (id_label) REFERENCES Label(id_label),
            FOREIGN KEY (id_dataSet) REFERENCES DataSet(id_dataSet)
        )
    """
    )

    # Create DataSet table
    cursor.execute(
        """
        CREATE TABLE DataSet (
            id_dataSet INTEGER PRIMARY KEY AUTOINCREMENT,
            name_dataSet TEXT,
            date_creation DATE,
            classes TEXT
        )
    """
    )

    # Commit changes and close connection
    connection.commit()
    connection.close()


from datetime import datetime


def create_dataset(name_dataSet, classes):
    # Connect to the SQLite database
    connection = sqlite3.connect("OD.db")
    cursor = connection.cursor()

    # Get the current date
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Insert a new dataset into the DataSet table
    cursor.execute(
        """
        INSERT INTO DataSet (name_dataSet, date_creation, classes)
        VALUES (?, ?, ?)
    """,
        (name_dataSet, current_date, classes),
    )

    # Commit changes and close connection
    connection.commit()
    connection.close()

    return cursor.lastrowid


def delete_dataset(dataset_id):
    # Connect to the SQLite database
    connection = sqlite3.connect("OD.db")
    cursor = connection.cursor()

    # Retrieve image_ids and label_ids associated with the dataset
    cursor.execute(
        """
        SELECT id_image, id_label FROM Image WHERE id_dataSet = ?
    """,
        (dataset_id,),
    )

    results = cursor.fetchall()

    # Delete each image and its associated label
    for image_id, label_id in results:
        cursor.execute(
            """
            DELETE FROM Image WHERE id_image = ?
        """,
            (image_id,),
        )

        cursor.execute(
            """
            DELETE FROM Label WHERE id_label = ?
        """,
            (label_id,),
        )

    # Delete the dataset from the DataSet table
    cursor.execute(
        """
        DELETE FROM DataSet WHERE id_dataSet = ?
    """,
        (dataset_id,),
    )

    # Commit changes
    connection.commit()

    # Close connection
    connection.close()


def get_dataset_classes(dataset_id):
    # Connect to the SQLite database
    connection = sqlite3.connect("OD.db")
    cursor = connection.cursor()

    # Retrieve the classes for the specified dataset
    cursor.execute(
        """
        SELECT classes FROM DataSet WHERE id_dataSet = ?
    """,
        (dataset_id,),
    )

    classes = cursor.fetchone()[0]

    # Close connection
    connection.close()

    return classes


def merge_datasets(dataset_id1, dataset_id2, dataset_name):
    # Retrieve classes for both datasets
    classes1 = get_dataset_classes(dataset_id1)
    classes2 = get_dataset_classes(dataset_id2)

    # Verify that both datasets have the same classes
    if classes1 != classes2:
        raise ValueError("Both datasets must have the same classes for merging.")

    # Connect to the SQLite database
    connection = sqlite3.connect("OD.db")
    cursor = connection.cursor()

    # Get information about the datasets to be merged
    cursor.execute("SELECT * FROM DataSet WHERE id_dataSet=?", (dataset_id1,))
    dataset1 = cursor.fetchone()
    cursor.execute("SELECT * FROM DataSet WHERE id_dataSet=?", (dataset_id2,))
    dataset2 = cursor.fetchone()

    # Create a new dataset with concatenated names
    new_dataset_name = dataset_name
    new_dataset_date = datetime.now().strftime("%Y-%m-%d")
    new_dataset_classes = classes1

    # Insert the new dataset into the DataSet table
    cursor.execute(
        "INSERT INTO DataSet (name_dataSet, date_creation, classes) VALUES (?, ?, ?)",
        (new_dataset_name, new_dataset_date, new_dataset_classes),
    )

    # Get the ID of the newly inserted dataset
    cursor.execute("SELECT last_insert_rowid()")
    new_dataset_id = cursor.fetchone()[0]

    # Retrieve (image, label) pairs in the dataset
    cursor.execute(
        """
        SELECT Image.*, Label.*
        FROM Image
        LEFT JOIN Label ON Image.id_label = Label.id_label
        WHERE (Image.id_dataSet in (?, ?) ) AND Image.id_label NOT NULL
    """,
        (dataset_id1, dataset_id2),
    )

    image_label_pairs = cursor.fetchall()

    # Retrieve non-labeled images in the dataset
    cursor.execute(
        """
        SELECT Image.*
        FROM Image
        WHERE (id_dataSet in (?, ?)) AND id_label IS NULL
    """,
        (dataset_id1, dataset_id2),
    )

    non_labeled_images = cursor.fetchall()

    # Insert labels first into the new dataset, and then associate them with images
    for image_label_pair in image_label_pairs:
        new_label_name = f"{new_dataset_name}{image_label_pair[10]}"
        # Insert the duplicated label into the new dataset
        cursor.execute(
            """
            INSERT INTO Label (name_label, label, size_label, augmented_label)
            VALUES (?, ?, ?, ?)
            """,
            (
                new_label_name,
                image_label_pair[9],
                image_label_pair[10],
                image_label_pair[11],
            ),
        )

        # Get the ID of the newly inserted label
        cursor.execute("SELECT last_insert_rowid()")
        new_label_id = cursor.fetchone()[0]
        # Insert the associated image into the new dataset with the new label id
        new_image_name = f"{new_dataset_name}{image_label_pair[1]}"
        cursor.execute(
            """
            INSERT INTO Image (name_image, image, size_image, augmented_image, id_label, id_dataSet)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                new_image_name,
                image_label_pair[2],
                image_label_pair[3],
                image_label_pair[4],
                new_label_id,
                new_dataset_id,
            ),
        )

    # Insert non_labeled_images into the new dataset without associated label
    for non_labeled_image in non_labeled_images:
        new_image_name = f"{new_dataset_name}{non_labeled_image[1]}"

        # Insert the duplicated image into the new dataset without associated label
        cursor.execute(
            """
            INSERT INTO Image (name_image, image, size_image, augmented_image, id_label, id_dataSet)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                new_image_name,
                non_labeled_image[2],
                non_labeled_image[3],
                non_labeled_image[4],
                None,
                new_dataset_id,
            ),
        )

    # Commit changes
    connection.commit()

    # Close connection
    connection.close()


def dataset_info(dataset_id):
    # Connect to the SQLite database
    connection = sqlite3.connect("OD.db")
    cursor = connection.cursor()

    # Get the number of labels in the dataset
    cursor.execute(
        """
        SELECT COUNT(DISTINCT id_label) FROM Image WHERE id_dataSet = ?
    """,
        (dataset_id,),
    )
    num_labels = cursor.fetchone()[0]

    # Get the number of labeled images in the dataset
    cursor.execute(
        """
        SELECT COUNT(DISTINCT id_image) FROM Image WHERE id_dataSet = ? AND id_label IS NOT NULL
    """,
        (dataset_id,),
    )
    num_labeled_images = cursor.fetchone()[0]

    # Get the number of unlabeled images in the dataset
    cursor.execute(
        """
        SELECT COUNT(DISTINCT id_image) FROM Image WHERE id_dataSet = ? AND id_label IS NULL
    """,
        (dataset_id,),
    )
    num_unlabeled_images = cursor.fetchone()[0]

    # Get the number of augmented images in the dataset
    cursor.execute(
        """
        SELECT COUNT(DISTINCT id_image) FROM Image WHERE id_dataSet = ? AND augmented_image = 1
    """,
        (dataset_id,),
    )
    num_augmented_images = cursor.fetchone()[0]

    # Get the number of augmented labels in the dataset
    cursor.execute(
        """
        SELECT COUNT(DISTINCT id_label) FROM Label WHERE id_label IN (
            SELECT id_label FROM Image WHERE id_dataSet = ? AND augmented_image = 1
        )
    """,
        (dataset_id,),
    )
    num_augmented_labels = cursor.fetchone()[0]

    # Get the total size of the dataset
    cursor.execute(
        """
        SELECT SUM(size_image) FROM Image WHERE id_dataSet = ?
    """,
        (dataset_id,),
    )
    total_size = cursor.fetchone()[0]

    # Get information about the dataset
    cursor.execute(
        """
        SELECT name_dataSet, date_creation, classes FROM DataSet WHERE id_dataSet = ?
    """,
        (dataset_id,),
    )
    dataset_info = cursor.fetchone()

    # Close connection
    connection.close()

    # Return the gathered information
    return {
        "num_labels": num_labels,
        "num_labeled_images": num_labeled_images,
        "num_unlabeled_images": num_unlabeled_images,
        "num_augmented_images": num_augmented_images,
        "num_augmented_labels": num_augmented_labels,
        "total_size": total_size,
        "date_creation": dataset_info[1],
        "name": dataset_info[0],
        "classes": dataset_info[2],
    }


def insert_image_and_label(image_file, label_file, dataset_id, augmented):
    # Connect to the SQLite database
    connection = sqlite3.connect("OD.db")
    cursor = connection.cursor()

    # Get the current date
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Insert label into Label table if it is not empty
    if label_file.getvalue():
        cursor.execute(
            """
            INSERT INTO Label (name_label, label, size_label, augmented_label)
            VALUES (?, ?, ?, ?)
        """,
            (label_file.name, label_file.read(), len(label_file.getvalue()), augmented),
        )
        label_id = cursor.lastrowid  # Retrieve the label_id

    else:
        label_id = None  # Set label_id to None if no label is provided

    # Insert image into Image table
    cursor.execute(
        """
        INSERT INTO Image (name_image, image, size_image, augmented_image, id_dataSet, id_label)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        (
            image_file.name,
            image_file.read(),
            len(image_file.getvalue()),
            augmented,
            dataset_id,
            label_id,  # Use the retrieved label_id
        ),
    )

    # Commit changes and close connection
    connection.commit()
    connection.close()


def delete_image_and_label(image_id):
    # Connect to the SQLite database
    connection = sqlite3.connect("OD.db")
    cursor = connection.cursor()

    # Retrieve the associated label_id and dataset_id
    cursor.execute(
        """
        SELECT id_label, id_dataSet FROM Image WHERE id_image = ?
    """,
        (image_id,),
    )

    result = cursor.fetchone()

    if result:
        label_id, dataset_id = result

        # Delete the image from the Image table
        cursor.execute(
            """
            DELETE FROM Image WHERE id_image = ?
        """,
            (image_id,),
        )

        # Delete the associated label from the Label table
        cursor.execute(
            """
            DELETE FROM Label WHERE id_label = ?
        """,
            (label_id,),
        )

        # If the dataset has no more images, you might want to delete it as well
        cursor.execute(
            """
            DELETE FROM DataSet WHERE id_dataSet = ? AND NOT EXISTS (
                SELECT 1 FROM Image WHERE id_dataSet = ?
            )
        """,
            (dataset_id, dataset_id),
        )

        # Commit changes
        connection.commit()

    # Close connection
    connection.close()


def delete_non_labeled(dataset_id):
    # Connect to the SQLite database
    connection = sqlite3.connect("OD.db")
    cursor = connection.cursor()

    # Retrieve the associated label_id and dataset_id
    cursor.execute(
        """
        DELETE FROM Image WHERE id_dataSet = ? AND id_label IS NULL
    """,
        (dataset_id,),
    )

    # Commit changes
    connection.commit()

    # Close connection
    connection.close()


def add_label(label_data, image_id):
    # Connect to the SQLite database
    connection = sqlite3.connect("OD.db")
    cursor = connection.cursor()

    # Insert the label into the Label table
    cursor.execute(
        """
        INSERT INTO Label (name_label, label, size_label, augmented_label)
        VALUES (?, ?, ?, ?)
    """,
        ("example_label.txt", label_data, len(label_data), 0),
    )  # Replace "example_label.txt" with the actual label name

    label_id = cursor.lastrowid

    # Associate the label with the specified image
    cursor.execute(
        """
        UPDATE Image SET id_label = ? WHERE id_image = ?
    """,
        (label_id, image_id),
    )

    # Commit changes
    connection.commit()

    # Close connection
    connection.close()


def get_dataset(dataset_id):
    # Connect to the SQLite database
    connection = sqlite3.connect("OD.db")
    cursor = connection.cursor()

    # Retrieve (image, label) pairs in the dataset
    cursor.execute(
        """
        SELECT Image.id_image, Image.name_image, Image.image, Label.label, Label.name_label
        FROM Image
        LEFT JOIN Label ON Image.id_label = Label.id_label
        WHERE Image.id_dataSet = ? AND Image.id_label NOT NULL
    """,
        (dataset_id,),
    )

    image_label_pairs = []
    for row in cursor.fetchall():
        id, image_name, image_data, label_data, label_name = row
        image_file = NamedBytesIO(image_data, name=image_name)
        label_file = NamedBytesIO(label_data, label_name) if label_data else None
        image_label_pairs.append((id, (image_file, label_file)))

    # Retrieve non-labeled images in the dataset
    cursor.execute(
        """
        SELECT Image.id_image, name_image, image
        FROM Image
        WHERE id_dataSet = ? AND id_label IS NULL
    """,
        (dataset_id,),
    )

    non_labeled_images = []
    for row in cursor.fetchall():
        id, image_name, image_data = row
        image_file = NamedBytesIO(image_data, name=image_name)
        non_labeled_images.append((id, image_file))

    # Close connection
    connection.close()

    return image_label_pairs, non_labeled_images


def get_all_datasets():
    # Connect to the SQLite database
    connection = sqlite3.connect("OD.db")
    cursor = connection.cursor()

    # Retrieve all datasets
    cursor.execute("SELECT * FROM DataSet")
    datasets = cursor.fetchall()

    # Close connection
    connection.close()

    return datasets
