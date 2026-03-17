# sourcing/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.sourcing_home, name='sourcing_home'),
    path('add/', views.add_supplier, name='add_supplier'),
    path('<int:pk>/', views.supplier_detail, name='supplier_detail'),
    path('<int:pk>/add/', views.add_procurement, name='add_procurement'),
    path('compare/', views.price_comparison, name='price_comparison'),
]