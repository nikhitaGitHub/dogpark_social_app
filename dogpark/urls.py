from django.urls import path
from dogpark import views

app_name='dogpark'

urlpatterns = [
    path('',views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('people/', views.people, name='people'),
    path('mypark/', views.mypark, name='mypark'),
    path('my_friends/', views.myFriends.as_view(), name="my_friends"),
    path('see_friend_requests/', views.seeFriendRequests.as_view(), name='see_friend_requests'),
    path('send_friend_request/', views.SendFriendRequest.as_view(), name='send_friend_request'),
    path('register/dogregisterform/<int:num>/', views.get_dog_form, name="dog_form"),
    path('accept_request/', views.AcceptRequests.as_view(), name="accept_request"),
    path('park_events/', views.park_events, name="park_events"),
    path('park_goals/', views.park_goals, name="park_goals"),
    path('attend_event/', views.attend_event, name="attend_event"),
    path('decline_event/', views.decline_event, name="decline_event"),
    path('add_goal/', views.add_goal, name="add_goal"),
    path('finish_goal/', views.finish_goal, name="finish_goal"),
    path('remove_goal/', views.remove_goal, name="remove_goal"),
    path('achievements/', views.achievements, name="achievements"),
    path('check_in/', views.check_in.as_view(), name="check_in"),
    path('check_out/', views.check_out.as_view(), name="check_out"),
    path('my_pet/', views.my_pet, name="my_pet")
    #This is restricted area, only loggen in users can see the homepage
    #Based on location , update dashboard view to mypark
    #path('') 
]