from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponse, JsonResponse
from .models import regu_connection
import os
from .sakshi import getkeyword
from .ritesh import processData
import json
from django.views.decorators.csrf import csrf_exempt
from db_connection import regulations_collection
from .utils import load_json_data
from django.views import View


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


@csrf_exempt
def getProductCategories(request):
    if request.method == 'GET':
        product_name = request.GET.get('product', None)
        if not product_name:
            return JsonResponse({'error': 'Product name not provided'}, status=400)

        # Search for the product in the database
        product_data = regulations_collection.find_one({product_name: {'$exists': True}})
        
        if not product_data:
            return JsonResponse({'error': 'Product not found'}, status=404)
        
        # Extract categories
        categories = list(product_data[product_name].keys())
        
        return JsonResponse({'categories': categories}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)



@csrf_exempt
def getRegulationsFromCategory(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_name = data.get('product')
            categories = data.get('categories')
            
            if not product_name or not categories:
                return JsonResponse({'error': 'Product name or categories not provided'}, status=400)
            
            # Search for the product in the database
            product_data = regulations_collection.find_one({product_name: {'$exists': True}})
            
            if not product_data:
                return JsonResponse({'error': 'Product not found'}, status=404)
            
            # Extract regulations for the specified categories
            regulations = {category: product_data[product_name].get(category, []) for category in categories}
            
            return JsonResponse({'product_name': product_name, 'regulations': regulations}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def run_algorithm():
    # Sample output from your algorithm
    data = {
        "product": "XYZ",
        "categories": {
            "category42": ["regulation112", "regulation122", "regulation132", "regulation142"],
            "category52": ["regulation152", "regulation162"]
        }
    }
    return data

@csrf_exempt
def save_algorithm_output(request):
    if request.method == 'POST':
        try:
            # Run the algorithm to get data
            data = run_algorithm()
            product = data['product']
            categories = data['categories']
            
            # Prepare data in the required format
            formatted_data = {product: categories}
            
            # Save the data to MongoDB
            result = regulations_collection.insert_one(formatted_data)
            
            # Convert ObjectId to string for JSON serialization
            formatted_data['_id'] = str(result.inserted_id)
            
            return JsonResponse({'status': 'success', 'data': formatted_data}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)