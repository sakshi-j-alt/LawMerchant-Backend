from django.urls import path 
from . import views

urlpatterns = [
    path('',views.lawMerchantApi,name="lawMerchantApi"),
    path('add',views.add,name="test_db")
]