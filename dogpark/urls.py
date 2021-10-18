from django.urls import path
from dogpark import views

app_name='dogpark'

urlpatterns = [
    path('',views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'), #This is restricted area, only loggen in users can see the homepage
    #Based on location , update dashboard view to mypark
    #path('') 
]