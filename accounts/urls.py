from django.urls import path 
from django.conf.urls import url
from .views import register,login,logout
urlpatterns = [
    path("register",register,name ='register'),
    path("login",login,name='login'),
    path("logout",logout,name='login') 

]
