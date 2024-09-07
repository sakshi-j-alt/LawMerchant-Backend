import json
import enchant
import nltk
import enchant

nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

def check_product_name(product_name):
    dictionary = enchant.Dict("en_US")
    
    if dictionary.check(product_name):
        tokens = nltk.word_tokenize(product_name)
        
        pos_tags = nltk.pos_tag(tokens)
        
        if pos_tags[0][1] in ['NN', 'NNS', 'NNP', 'NNPS']:
            return True
    
    return False

def getkeyword(product, json_file='templates/keywords.json'):
    with open(json_file, 'r') as file:
        keywords = json.load(file)
    
    result_array = [product]
    
    flat_keywords = {key: value for item in keywords for key, value in item.items()}
    
    if product in flat_keywords:
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



def checkPreviouslyProcessed(keywords, json_file='myapp\dummy_regulations.json'):
    # Load the JSON data from the file
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    result = []
    regulations = set()

    for keyword in keywords:
        if keyword in data:
            result.append(keyword)
            regulations.update(data[keyword])

    result.extend(sorted(regulations))

    return result


