import os
import re
import spacy
import nltk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import nltk
import enchant

# Download necessary NLTK data
nltk.download('punkt')

# Load SpaCy model
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    from spacy.cli import download
    download('en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        # Try reading with a different encoding
        with open(file_path, 'r', encoding='latin-1') as file:
            return file.read()

def getkeyword(product, json_file='templates/keywords.json'):
    # Load the JSON data from the file
    with open(json_file, 'r') as file:
        keywords = json.load(file)
    
    # Create a new list to avoid modifying the input list directly
    result_array = [product]
    
    # Flatten the keywords dictionary
    flat_keywords = {key: value for item in keywords for key, value in item.items()}
    
    # Iterate over the input product array
    
    if product in flat_keywords:
        # Append the corresponding values to the result array
        result_array.extend(flat_keywords[product])
    
    return result_array

def remove_duplicates(strings):
    seen = set()
    result = []
    for string in strings:
        lower_string = string.lower()
        if lower_string not in seen:
            seen.add(lower_string)
            result.append(string)
    return result


def extract_product_sections(text, product):
    extracted_sections = []
    for product_keyword in product: 
        pattern = re.compile(
            rf'(?i)(^.*?{re.escape(product_keyword)}.*?)(?=\n[A-Z][^a-z]|\n[0-9]+\.\s|\Z)',
            re.DOTALL | re.MULTILINE
        )
        matches = pattern.findall(text)
        
        if matches:
            for i, match in enumerate(matches):
                match = match.strip()
                doc = nlp(match)
                sentences = [sent.text for sent in doc.sents]
                relevant_sentences = []
                for sent in sentences:
                    if product_keyword.lower() in sent.lower():
                        relevant_sentences.append(sent)
                    elif relevant_sentences and re.match(r'^[a-zA-Z0-9]\.', sent.strip()):
                        relevant_sentences.append(sent)
                section_text = ' '.join(relevant_sentences)
                extracted_sections.append(section_text)

    return extracted_sections

def process_all_files(base_dir, product_name, product):
    result = {
        "product": product_name,
        "categories": {}
    }

    for category in os.listdir(base_dir):
        category_path = os.path.join(base_dir, category)
        if os.path.isdir(category_path):
            file_path = os.path.join(category_path, 'regulations.txt')
            if os.path.isfile(file_path):
                regulations_text = read_file(file_path)
                sections = extract_product_sections(regulations_text, product)
                if sections:
                    result["categories"][category] = sections

    return result

def run_algo(product_name, base_dir):
    # Process all files and get the result
    product = getkeyword(product_name)
    product = remove_duplicates(product)
    result = process_all_files(base_dir, product_name, product)
    return result

# Example usage
base_dir = 'C:\\A Personal Files\\LawMerchant-Backend\\food'
product_name = 'milk'
predictions = run_algo(product_name, base_dir)

# Convert predictions to a DataFrame
def convert_to_dataframe(predictions):
    data = []
    for category, sections in predictions["categories"].items():
        for section in sections:
            data.append({
                "category": category,
                "section_length": len(section.split()),  # Number of words in the section
                "section_text": section
            })
    return pd.DataFrame(data)

df = convert_to_dataframe(predictions)

# Display the first few rows of the DataFrame
print(df.head())

# Histograms for Data Distribution
def plot_histograms(df):
    df['section_length'].hist(bins=30, figsize=(10, 6))
    plt.xlabel('Section Length')
    plt.ylabel('Frequency')
    plt.title('Data Distribution - Section Length')
    plt.show()

plot_histograms(df)

# Box Plots for Data Distribution
def plot_boxplots(df):
    df.boxplot(column='section_length', by='category', figsize=(10, 6))
    plt.xlabel('Category')
    plt.ylabel('Section Length')
    plt.title('Data Distribution - Section Length by Category')
    plt.suptitle('')
    plt.show()

plot_boxplots(df)


# For simplicity, let's add a dummy feature for demonstration
df['dummy_feature'] = np.random.rand(len(df))

# Scatter Plots for Feature Analysis
def plot_scatter(df):
    sns.scatterplot(x='section_length', y='dummy_feature', hue='category', data=df)
    plt.xlabel('Section Length')
    plt.ylabel('Dummy Feature')
    plt.title('Feature Analysis - Scatter Plot')
    plt.show()

plot_scatter(df)

# Pair Plots for Feature Analysis
def plot_pair(df):
    sns.pairplot(df, hue='category', vars=['section_length', 'dummy_feature'])
    plt.suptitle('Feature Analysis - Pair Plot', y=1.02)
    plt.show()

plot_pair(df)
