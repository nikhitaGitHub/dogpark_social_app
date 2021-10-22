from django.urls import path
from dogpark import views
app_name='dogpark'

urlpatterns = [
    path('',views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('people/', views.people, name='people'),
    path('register/dogregisterform/', views.get_dog_form, name="dog_form"),
    path('send_friend_request/', views.SendFriendRequest.as_view(), name="send_friend_request")
    #This is restricted area, only loggen in users can see the homepage
    #Based on location , update dashboard view to mypark
    #path('') 
]