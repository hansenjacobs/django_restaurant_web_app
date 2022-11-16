from django.urls import path
from . import views

urlpatterns = [
    path('registeruser/', views.registerUser, name='registerUser'),
    path('registervendor/', views.registerVendor, name='registerVendor'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('customerdashboard/', views.customerdashboard, name='customerdashboard'),
    path('vendordashboard/', views.vendordashboard, name='vendordashboard'),
    path('myaccount/', views.myAccount, name='myAccount'),
]
