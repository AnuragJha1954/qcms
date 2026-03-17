# khata/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.khata_home, name='khata_home'),
    path('add/', views.add_party, name='add_party'),
    path('<int:pk>/', views.party_detail, name='party_detail'),
    path('<int:pk>/add-entry/', views.add_entry, name='add_entry'),
    path('<int:pk>/settle/', views.settle_payment, name='settle_payment'),
]