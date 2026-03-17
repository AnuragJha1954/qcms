# quality/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.quality_home, name='quality_home'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('<int:pk>/add-param/', views.add_parameter, name='add_parameter'),
    path('<int:pk>/add-check/', views.add_check, name='add_check'),
    path('add/', views.add_product, name='add_product'),
]