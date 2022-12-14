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
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
    path('resetpassword/<uidb64>/<token>', views.resetpasswordvalidation, name='resetpasswordvalidation'),
    path('resetpassword/', views.resetpassword, name='resetpassword'),
]
