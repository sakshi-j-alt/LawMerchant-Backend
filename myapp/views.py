from django.shortcuts import render, HttpResponse
from .models import regu_connection

def lawMerchantApi (request) : 
    return HttpResponse("hello world")


# Create your views here.
def add (request) :
    record= {
        "name" :"sakshi"
    }
    regu_connection.insert_one(record)
    return HttpResponse("new persone added")