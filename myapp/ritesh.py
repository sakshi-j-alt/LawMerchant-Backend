import os
from pymongo import MongoClient

# MongoDB connection settings
client = MongoClient('mongodb://localhost:27017/')
db = client['Lawmerchant']  # Replace 'your_database' with your database name
collection = db['regulations']  # Replace 'text_collection' with your collection name

# Directory where your text files are located
directory = 'C:/Users/ADITYA/OneDrive/Desktop/law merchant/Packaging'

def store_text_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            category_name = os.path.splitext(filename)[0]  # Use filename without extension as category name

            # Read text content from file
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                text_content = file.read()

            # Store data in MongoDB
            document = {
                'category': category_name,
                'text': text_content
            }
            collection.insert_one(document)
            print(f'Stored text from file {filename} in MongoDB')

if __name__ == '__main__':
    store_text_files(directory)
