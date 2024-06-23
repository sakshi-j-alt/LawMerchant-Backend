from django.urls import path 
from . import views

urlpatterns = [
    path('',views.lawMerchantApi,name="lawMerchantApi"),
    path('add',views.add,name="add"),
    path('uploadFile', views.render_upload_form),
    path('extractData',views.extractData)
]