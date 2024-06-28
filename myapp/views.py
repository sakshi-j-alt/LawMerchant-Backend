from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponse, JsonResponse
from .models import regu_connection
import os
from .sakshi import getkeyword
from .ritesh import processData
import json
from django.views.decorators.csrf import csrf_exempt
from .match import run_algorithm
from db_connection import ppd

def lawMerchantApi (request) : 
    return HttpResponse("hello world")

def render_upload_form(request):
    return render(request, 'upload_file.html')

def add(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        if uploaded_file.name.endswith('.txt'):
            category_name = os.path.splitext(uploaded_file.name)[0]  # Use filename without extension as category name

            # Read text content from file
            text_content = uploaded_file.read().decode('utf-8')

            # Store data in MongoDB
            document = {
                'category': category_name,
                'text': text_content
            }
            regu_connection.insert_one(document)
            print(f'Stored text from file {uploaded_file.name} in MongoDB')
            return HttpResponse("Data Added in Database")
        else:
            return HttpResponse("Please upload a .txt file", status=400)
    else:
        return HttpResponse("No file uploaded or invalid request", status=400)
    
product_array = []
def extractData(request):
    product_name = request.POST.get('productName','')
    if product_name:
        product_array = ["regulation", product_name]
        keywords = getkeyword(product_array)
        result = processData(keywords)
        for r in keywords :
            print (r+"\n")
        return HttpResponse(result)
    
    else:
        return HttpResponse("No product name provided", status=400)

from .utils import load_json_data

data = load_json_data()

# def search_view(request):
#     if request.method == 'POST':
#         product = request.POST.get('product').lower()
#         if product in data:
#             categories = list(data[product].keys())
            
#             return HttpResponse(categories)
#             # return render(request, 'select_categories.html', {'product': product, 'categories': categories})
#         else:
#             return render(request, 'search.html', {'error': 'Product not found'})
#     return render(request, 'search.html')

# def categories_view(request):
#     if request.method == 'POST':
#         product = request.POST.get('product')
#         categories_str = request.POST.get('categories')
        
#         try:
#             selected_categories = json.loads(categories_str)
#         except json.JSONDecodeError:
#             return HttpResponse("Invalid categories format. It should be a JSON array.", status=400)
        
#         # Ensure product and selected categories are valid
#         if product in data and all(cat in data[product] for cat in selected_categories):
#             regulations = {cat: data[product][cat] for cat in selected_categories}
#             return JsonResponse(regulations)
#         else:
#             return HttpResponse("Invalid product or categories", status=400)
       
#     return redirect('search')

# def save_json_data(data):
#     json_file_path = os.path.join(os.path.dirname(__file__), 'dummy_regulations.json')
#     with open(json_file_path, 'w') as file:
#         json.dump(data, file, indent=4)

# @csrf_exempt
# def add_regulation_view(request):
#     if request.method == 'POST':
#         try:
#             request_data = json.loads(request.body)
#             product = request_data['product']
#             categories = request_data['categories']

#             data = load_json_data()

#             if product not in data:
#                 data[product] = {}

#             for category, regulations in categories.items():
#                 if category not in data[product]:
#                     data[product][category] = []
#                 data[product][category].extend(regulations)

#             save_json_data(data)
#             return JsonResponse({"message": "Data added successfully"}, status=200)
#         except KeyError as e:
#             return HttpResponse(f"Missing key: {e}", status=400)
#         except json.JSONDecodeError:
#             return HttpResponse("Invalid JSON format", status=400)
#         except Exception as e:
#             return HttpResponse(f"An error occurred: {e}", status=500)
#     return HttpResponse("Invalid request method", status=405)


def search_view(request):
    if request.method == 'POST':
        product = request.POST.get('product').lower()
        # Query MongoDB collection
        result = ppd.find_one({"product": product})

        if result:
            categories = [entry['category'] for entry in result['regulations']]
            return JsonResponse(categories, safe=False)
            # return render(request, 'select_categories.html', {'product': product, 'categories': categories})
        else:
            return render(request, 'search.html', {'error': 'Product not found'})
    return render(request, 'search.html')

@csrf_exempt
def categories_view(request):
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body)
            product = request_data['product']
            categories = request_data['categories']

            # Ensure product and selected categories are valid
            result = ppd.find_one({"product": product})

            if result:
                valid_categories = result['categories'].keys()
                for cat in categories:
                    if cat not in valid_categories:
                        return HttpResponse(f"Invalid category: {cat} for product: {product}", status=400)

                regulations = {cat: result['categories'][cat] for cat in categories}
                return JsonResponse(regulations)
            else:
                return HttpResponse("Invalid product or categories", status=400)
        except KeyError as e:
            return HttpResponse(f"Missing key: {e}", status=400)
        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON format", status=400)
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}", status=500)
    return HttpResponse("Invalid request method", status=405)

@csrf_exempt
def add_regulation_view(request):
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body)
            product = request_data['product']
            categories = request_data['categories']

            # Ensure product exists in MongoDB
            result = ppd.find_one({"product": product})

            if not result:
                ppd.insert_one({"product": product, "categories": {}})

            # Update categories with regulations
            for category, regulations in categories.items():
                ppd.update_one({"product": product}, {"$addToSet": {"categories." + category: {"$each": regulations}}})

            return JsonResponse({"message": "Data added successfully"}, status=200)
        except KeyError as e:
            return HttpResponse(f"Missing key: {e}", status=400)
        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON format", status=400)
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}", status=500)
    return HttpResponse("Invalid request method", status=405)


@csrf_exempt
def save_algorithm_output(request):
    if request.method == 'POST':
        try:
            # Run the algorithm to get data
            data = run_algorithm()
            product = data['product']
            categories = data['categories']
            
            for category, regulations in categories.items():
                ppd.insert_one({
                    "product": product,
                    "category": category,
                    "regulations": regulations
                })

            return JsonResponse({"message": "Data saved to MongoDB successfully"})
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=500)
    
    return HttpResponse("Only POST method is allowed", status=405)