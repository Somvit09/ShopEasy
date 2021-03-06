from django.urls import path
from . import views
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signin/', views.signin, name='signin'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),

    # email verification
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('reset_password_validation/<uidb64>/<token>/', views.reset_password_validation, name='reset_password_validation'),
]