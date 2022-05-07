from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('clients/', views.clients, name='clients'),
    path('vendors/', views.vendors, name='vendors'),
    path('products/', views.products, name='products'),
    path('clients/buy/', views.buy_products, name='buy_products'),
    path('clients/recomendation/', views.recomendations, name='recomendations'),
    path('products/tops/<int:x>/', views.top_products, name='top_products'),
    #path('', views., name='')
]