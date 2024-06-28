from django.urls import path 
from . import views

urlpatterns = [
    path('',views.lawMerchantApi,name="lawMerchantApi"),
    path('add',views.add,name="add"),
    path('uploadFile', views.render_upload_form),
    path('extractData',views.extractData),
    path('search', views.search_view, name='search'),
    path('categories', views.categories_view, name='categories'),
     path('add-regulation', views.add_regulation_view, name='add_regulation'),
     path('save_algorithm_output', views.save_algorithm_output, name='save_algorithm_output'),
]