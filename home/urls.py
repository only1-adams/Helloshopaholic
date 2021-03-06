from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('category/', views.category, name='category'),
    path('products/<str:id>/<slug:slug>', views.prod_list, name='prod_list'),
    path('products-details/<str:id>/<slug:slug>', views.prod_detail, name='prod_detail'),
]