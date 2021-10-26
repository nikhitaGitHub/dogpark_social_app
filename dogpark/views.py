from django.forms.widgets import PasswordInput
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from dogpark.models import Friendship, Owner, Dog, FriendRequest
from dogpark.forms import UserForm, UserProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.urls import reverse
import os

# Create your views here.
def index(request):
    context_dict = {}
    return render(request, 'dogpark/index.html', context=context_dict)

def user_login(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                 login(request,user)
                 return redirect(reverse('dogpark:index'))
            else:
                return HttpResponse("Your account is disabled")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied")
    else:
        return render(request, 'dogpark/index.html')
 
@login_required   
def user_logout(request):
    logout(request)
    return redirect(reverse('dogpark:index'))

def get_dog_form(request):
    form = UserProfileForm()
    context = {
        "form": form
    }
    template =render_to_string('forms.html', context=context)# render_to_string('forms.html', context=context)
    return JsonResponse({"form": template})

def register(request):
    registered = False
    
    if request.method == 'POST':
        
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            x = User.objects.get(username=user.username)
            print(x)
            
            profile = profile_form.save(commit=False)  
            #profile_form. = user_form.num_dogs
            profile.owner = x
            
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
        
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    context_dict = {}
    context_dict['user_form'] = user_form
    context_dict['profile_form'] = profile_form
    context_dict['registered'] = registered
        
    return render(request, 'dogpark/register.html', context=context_dict)

@login_required
def dashboard():
    pass

@login_required
def people(request):
    user_list = User.objects.exclude(username=get_user(request))
    context_dict = {}
    context_dict['user_list'] = user_list
    return render(request, 'dogpark/people.html', context=context_dict)

class seeFriendRequests(View):
    @method_decorator(login_required)
    def get(self, request):
        context_dict = {}
        print("Inside funtion")
        my_requests = False
        fr = True
        u = get_user(request)
        if not request.user.is_anonymous:
            print("USer is not anonymous")
            try:
                my_requests = FriendRequest.objects.get(receiver=request.user)
                #my_requests = FriendRequest.objects.all().filter(receiver=request.user)
            except FriendRequest.DoesNotExist:
                fr = None
            if fr == None:
                print("redirecting to homepage")
                return redirect(reverse('dogpark:index'))
            context_dict['incoming_requests'] = my_requests
            return render(request, 'dogpark/see_friend_requests.html', context=context_dict)
    
class myFriends(View):
    @method_decorator(login_required)
    def get(self, request):
        context_dict = {}
        u = get_user(request)
        try:
            friendship = Friendship.objects.get(from_friend=u)
            friendship.extend(Friendship.objects.get(to_friend=u))
        except Friendship.DoesNotExist:
            friendship = None
        if friendship == None:
            return redirect(reverse('dogpark:index'))
        context_dict['friends'] = friendship
        return render(request,  'dogpark/my_friends.html', context=context_dict)
         
class SendFriendRequest(View):
    @method_decorator(login_required)
    def post(self,request):
        data = {'response' : -1}
        uname = request.POST.get('uname')
        try:
            sender = get_user(request)
            receiver = User.objects.get(username=uname)
            req_obj, created = FriendRequest.objects.get_or_create(sender=sender, receiver=receiver)
        except ValueError:
            return JsonResponse(data)
        return JsonResponse({'response': 1})
    
class AcceptRequests(View):
    @method_decorator(login_required)
    def post(self,request):
        print("Hitting the view")
        data = {'response': -1}
        uname = request.POST.get('uname')
        try:
            from_friend = request.user
            to_friend = User.objects.get(username=uname)
            friend, created = Friendship.objects.get_or_create(from_friend=from_friend, to_friend=to_friend)
            if created:
                return JsonResponse({'response': 1})
        except ValueError:
            return JsonResponse(data)
        return JsonResponse({'response': 1})