"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from .import views
from django.urls import path

urlpatterns = [
    path('register/', views.register.as_view(),name='register'),
    path('EmailResendOtp/', views.EmailResendOtp.as_view(),name='EmailResendOtp'),
    path('EmailOtpVerify/', views.EmailOtpVerify.as_view(),name='EmailOtpVerify'),
    path('MobileNoAdd/', views.MobileNoAdd.as_view(),name='MobileNoAdd'),
    path('MobileResendOtp/', views.MobileResendOtp.as_view(),name='MobileResendOtp'),
    path('MobileOtpVerify/', views.MobileOtpVerify.as_view(),name='MobileOtpVerify'),
    path('login/', views.login.as_view(),name='login'),
    path('loginOtpVerify/', views.loginOtpVerify.as_view(),name='loginOtpVerify'),
    path('Profile/', views.Profilecreate.as_view(),name='Profilecreate'),
    path('logout/', views.logout.as_view(),name='logout'),
    
    
    path('Admin_register/', views.Admin_register.as_view(),name='Admin_register'),
    path('AdminViewuser/', views.AdminViewuser.as_view(),name='AdminViewuser'),
    path('logincheck/', views.logincheck.as_view(),name='logincheck'),
    
   
]
