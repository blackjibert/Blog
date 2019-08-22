
from django.contrib import admin
from django.urls import path, include
from . import views
#应用的名称
app_name = 'userprofile'

urlpatterns = [
   path('login/', views.user_login, name='login'),
   path('logout/', views.user_logout, name='logout'),
   path('register/', views.user_register, name='register'),
   #用户信息
   path('edit/<int:id>/', views.user_edit, name='edit'),
]
