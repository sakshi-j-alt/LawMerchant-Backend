product_array = ["regulation", "pasta"]
import json

def getkeyword(productarray, json_file='myapp\keywords.json'):
    # Load the JSON data from the file
    with open(json_file, 'r') as file:
        keywords = json.load(file)
    
    # Create a new list to avoid modifying the input list directly
    result_array = productarray[:]
    
    # Iterate over the input product array
    for product in productarray:
        # Check if the product exists as a key in the JSON data
        if product in keywords:
            # Append the corresponding values to the result array
            result_array.extend(keywords[product])
    
    return result_array


print(getkeyword(product_array))



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

# Example usage
keywords = getkeyword(product_array)
output = checkPreviouslyProcessed(keywords)
print(output)
