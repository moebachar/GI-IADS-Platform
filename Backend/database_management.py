from sqlalchemy import (
    create_engine,
    ForeignKey,
    Column,
    Integer,
    String,
    CHAR,
    LargeBinary,
    inspect,
    MetaData,
    Table,
)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from io import BytesIO
from Importation import NamedBytesIO

Base = declarative_base()


class FilePair(Base):
    __tablename__ = "file_pairs"

    id = Column("id", String(1000), primary_key=True)
    image = Column("image", LargeBinary)
    label = Column("label", LargeBinary)

    def __init__(self, id, image, label):
        self.id = id
        self.image = image
        self.label = label

    def __repr__(self):
        return f"{self.id}"


engine = create_engine("sqlite:///mydb.db", echo=True)


def create_user_table(name, engine=engine):
    # Construct the table name
    table_name = f"filespairs_{name}"
    connection = engine.connect()

    # Check if the table already exists
    if not inspect(engine).has_table(table_name):
        # Create the table using the FilePair schema
        FilePair.__table__.name = table_name
        FilePair.__table__.create(bind=engine)

        # Close the connection
    connection.close()


def insert_files_into_user_table(name, files, engine=engine):
    # Construct the table name
    table_name = f"filespairs_{name}"

    # Check if the table exists

    if inspect(engine).has_table(table_name):
        # Bind the existing table to the FilePair class
        FilePair.__table__.name = table_name

        # Create a session
        Session = sessionmaker(bind=engine)
        session = Session()

        # Insert files into the user table
        for image, label in files:
            new_file = FilePair(
                id=image.name + "seperate_image_label" + label.name,
                image=image.getvalue(),
                label=label.getvalue(),
            )
            session.add(new_file)

        session.commit()
        session.close()
        print(f"Files inserted into {table_name}")
    else:
        print(f"Table {table_name} does not exist")


def extract_files_from_user_table(name, engine=engine):
    # Construct the table name
    table_name = f"filespairs_{name}"

    # Check if the table exists
    if inspect(engine).has_table(table_name):
        # Bind the existing table to the FilePair class
        FilePair.__table__.name = table_name

        # Create a session
        Session = sessionmaker(bind=engine)
        session = Session()

        # Query all files from the user table
        files = session.query(FilePair).all()

        # Extract data from the files
        extracted_files = []
        for line in files:
            image_name, label_name = line.id.split("seperate_image_label")
            extracted_files.append(
                (
                    NamedBytesIO(line.image, image_name),
                    NamedBytesIO(line.label, label_name),
                )
            )

        session.close()
        return extracted_files
    else:
        print(f"Table {table_name} does not exist")
        return None


def delete_table_by_name(name, engine=engine):
    table_name = f"filespairs_{name}"
    # Create a MetaData object
    metadata = MetaData()

    # Reflect the table from the database
    metadata.reflect(bind=engine)
    table = metadata.tables.get(table_name)

    if table is not None:
        # Drop the table
        table.drop(bind=engine)
        print(f"Table {table_name} has been deleted.")
    else:
        print(f"Table {table_name} does not exist.")
