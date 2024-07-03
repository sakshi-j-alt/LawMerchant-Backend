from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponse, JsonResponse
from .models import food,electronics,agriculture,hardware,general, reports
import os
from .modules import check_product_name
import json
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .algorithm import run_algo

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
            food.insert_one(document)
            print(f'Stored text from file {uploaded_file.name} in MongoDB')
            return HttpResponse("Data Added in Database")
        else:
            return HttpResponse("Please upload a .txt file", status=400)
    else:
        return HttpResponse("No file uploaded or invalid request", status=400)



@csrf_exempt
def getProductCategories(request):
    if request.method == 'GET':
        product_name = request.GET.get('product', None)
        product_type = request.GET.get('productType', None)
        if not product_name:
            return JsonResponse({'error': 'Product name not provided'}, status=400)

        # Search for the product in the database
        if(product_type == "food"):
            product_data = food.find_one({product_name: {'$exists': True}})
        # elif(product_type == "electronics"):
        #     product_data = electronics.find_one({product_name: {'$exists': True}})
        # elif(product_type == "agriculture"):
        #     product_data = agriculture.find_one({product_name: {'$exists': True}})
        # elif(product_type == "hardware"):
        #     product_data = hardware.find_one({product_name: {'$exists': True}})
        # elif(product_type == "general"):
        #     product_data = general.find_one({product_name: {'$exists': True}})
        else:
            return JsonResponse({'error': 'Category work in progress'}, status=400)


        if not product_data:
            if(check_product_name(product_name)):
                result = run_algo(product_name,product_type)
                save_algorithm_output(result,product_type)
                product_data = food.find_one({product_name: {'$exists': True}})
            else:
                return JsonResponse({'error': 'Product name is invalid'}, status=400)
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
            product_type = data.get('productType')
            categories = data.get('categories')
            
            if not product_name or not categories:
                return JsonResponse({'error': 'Product name or categories not provided'}, status=400)
            
            # Search for the product in the database
            if(product_type == "food"):
                product_data = food.find_one({product_name: {'$exists': True}})
            elif(product_type == "electronics"):
                product_data = electronics.find_one({product_name: {'$exists': True}})
            elif(product_type == "agriculture"):
                product_data = agriculture.find_one({product_name: {'$exists': True}})
            elif(product_type == "hardware"):
                product_data = hardware.find_one({product_name: {'$exists': True}})
            elif(product_type == "general"):
                product_data = general.find_one({product_name: {'$exists': True}})
            else:
                product_data = food.find_one({product_name: {'$exists': True}})

            
            if not product_data:
                return JsonResponse({'error': 'Product not found'}, status=404)
            
            # Extract regulations for the specified categories
            regulations = {category: product_data[product_name].get(category, []) for category in categories}
            
            return JsonResponse({'product_name': product_name, 'regulations': regulations}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)




@csrf_exempt
def save_algorithm_output(data,product_type):
    try:
        # Run the algorithm to get data
        product = data['product']
        categories = data['categories']
        
        # Prepare data in the required format
        formatted_data = {product: categories}
        
        # Save the data to MongoDB
        if(product_type == "food"):
            result = food.insert_one(formatted_data)
        elif(product_type == "electronics"):
            result = electronics.insert_one(formatted_data)
        elif(product_type == "agriculture"):
            result = agriculture.insert_one(formatted_data)
        elif(product_type == "hardware"):
            result = hardware.insert_one(formatted_data)
        elif(product_type == "general"):
            result = general.insert_one(formatted_data)
        else:
            result = food.insert_one(formatted_data)

        
        # Convert ObjectId to string for JSON serialization
        formatted_data['_id'] = str(result.inserted_id)
        
        
    except Exception as e:
        return e




@csrf_exempt
def report_regulation(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_name = data.get('product_name')
            category_name = data.get('category_name')
            regulation = data.get('regulation')
            answers = data.get('answers')
            regulation_applicable_for = data.get('regulation_applicable_for', None)
            other_suggestion = data.get('other_suggestion')

            # Validate required fields
            if not product_name or not category_name or not regulation or answers is None or other_suggestion is None:
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            # Prepare the document to insert
            report_data = {
                'product_name': product_name,
                'category_name': category_name,
                'regulation': regulation,
                'answers': answers,
                'other_suggestion': other_suggestion
            }

            # Conditionally add regulation_applicable_for if provided
            if regulation_applicable_for:
                report_data['regulation_applicable_for'] = regulation_applicable_for

            # Save the document in MongoDB
            reports.insert_one(report_data)

            return JsonResponse({'message': 'Report saved successfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
