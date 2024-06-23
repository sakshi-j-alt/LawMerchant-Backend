from django.shortcuts import render, HttpResponse
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

