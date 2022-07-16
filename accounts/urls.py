from django.urls import path
from . import views
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signin/', views.signin, name='signin'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),

    # email verification
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]