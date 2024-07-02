import json
import enchant

def check_product_name(product_name):
    # Create an English dictionary instance
    dictionary = enchant.Dict("en_US")
    
    # Check if the product name is a valid word
    if dictionary.check(product_name):
        return True
    else:
        return False

def getkeyword(product, json_file='keywords.json'):
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



def checkPreviouslyProcessed(keywords, json_file='myapp\dummy_regulations.json'):
    # Load the JSON data from the file
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    result = []
    regulations = set()

    # Iterate through the provided keywords
    for keyword in keywords:
        if keyword in data:
            # Add the keyword to the result list
            result.append(keyword)
            # Add the regulations for the matched keyword
            regulations.update(data[keyword])

    # Convert the set of regulations to a sorted list to ensure consistent order
    result.extend(sorted(regulations))

    return result


