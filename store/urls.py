from django.urls import path
from . import views

urlpatterns = [
    path('', views.storeHome, name='store'),
    path('<slug:category_slug>/', views.storeHome, name='product_by_categories'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product_details, name='product_details'),
]