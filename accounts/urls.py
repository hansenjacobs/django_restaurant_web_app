from django.urls import path
from . import views

urlpatterns = [
    path('registeruser/', views.registerUser, name='registerUser'),
    path('registervendor/', views.registerVendor, name='registerVendor'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
