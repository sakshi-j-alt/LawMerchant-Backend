from django.urls import path 
from . import views

urlpatterns = [
    path('',views.lawMerchantApi,name="lawMerchantApi"),
    path('add',views.add,name="add"),
    path('uploadFile', views.render_upload_form),
    path('getProductCategories', views.getProductCategories, name='getProductCategories'),
    path('getRegulationsFromCategory', views.getRegulationsFromCategory, name='getRegulationsFromCategory'),
    path('save_algorithm_output', views.save_algorithm_output, name='save_algorithm_output'),
    path('report_regulation', views.report_regulation, name='report_regulation')
]