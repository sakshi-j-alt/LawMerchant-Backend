from django.shortcuts import render, HttpResponse, redirect

from .models import regu_connection
import os
from .sakshi import getkeyword
from .ritesh import processData

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

def search_view(request):
    if request.method == 'POST':
        product = request.POST.get('product').lower()
        if product in data:
            categories = list(data[product].keys())
            
            return HttpResponse(categories)
            # return render(request, 'select_categories.html', {'product': product, 'categories': categories})
        else:
            return render(request, 'search.html', {'error': 'Product not found'})
    return render(request, 'search.html')

def categories_view(request):
    if request.method == 'POST':
        product = request.POST.get('product')
        selected_categories = request.POST.getlist('categories')
        
        # Ensure product and selected categories are valid
        if product in data and all(cat in data[product] for cat in selected_categories):
            regulations = {cat: data[product][cat] for cat in selected_categories}
            return HttpResponse(regulations)
        else:
            return HttpResponse("Invalid product or categories", status=400)
        # return render(request, 'display_regulations.html', {'product': product, 'regulations': regulations})
    return redirect('search')

# import json
# from django.http import HttpResponse, JsonResponse
# from django.shortcuts import redirect

# def categories_view(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             product = data.get('product')
#             selected_categories = data.get('categories', [])

#             # Assuming `data` is a dictionary containing your regulations
#             regulations = {cat: data[product][cat] for cat in selected_categories}
#             return JsonResponse(regulations)

#         except json.JSONDecodeError:
#             return HttpResponse("Invalid JSON", status=400)
#         except KeyError:
#             return HttpResponse("Invalid product or categories", status=400)
#         except Exception as e:
#             return HttpResponse(f"An error occurred: {str(e)}", status=500)

#     return redirect('search')

