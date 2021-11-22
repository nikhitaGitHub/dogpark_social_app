from re import U
from django.core.exceptions import ObjectDoesNotExist
from django.forms.formsets import formset_factory
from django.forms.widgets import PasswordInput
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from dogpark.models import Friendship, Owner, Dog, FriendRequest, Goals, Events, Achievement
from dogpark.forms import UserForm, UserProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.urls import reverse
from django.db.models import Q
import os
from django.forms import formset_factory


# Create your views here.
def index(request):
    context_dict = {}
    checked_in_friends = []
    u = request.user
    if not request.user.is_anonymous:
        friends = Friendship.objects.filter(Q(from_friend = u) | Q(to_friend = u))
        for x in friends.iterator():
            if x.from_friend == u:
                ci_u = x.to_friend
            else:
                ci_u = x.from_friend
            try:
                if Owner.objects.get(Q(user=ci_u) & Q(checked_in=True)):
                    checked_in_friends.append(ci_u)
            except Owner.DoesNotExist:
                context_dict["my_checked_in_friends"] = checked_in_friends
                context_dict["u"] = u
                return render(request, 'dogpark/index.html', context=context_dict)               
        context_dict["my_checked_in_friends"] = checked_in_friends
        context_dict["u"] = u
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

def get_dog_form(request, num):
    formset = formset_factory(UserProfileForm, extra=num)
    data = {
            'form-TOTAL_FORMS': str(num),
            'form-INITIAL_FORMS': '0' 
        }
    form = formset(data)
    context = {
        "form": form
    }
    template =render_to_string('forms.html', context=context)# render_to_string('forms.html', context=context)
    return JsonResponse({"form": template})

def register(request):
    registered = False
    profile_form = []
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            num = user_form.cleaned_data['num_dogs']
            profile_form_set = formset_factory(UserProfileForm, extra=int(num))
            Owner.objects.get_or_create(user = user, num_dogs = num)
            x = User.objects.get(username=user.username)
            profile_form = profile_form_set(request.POST)
            if profile_form.is_valid():
                for form in profile_form:
                    profile = form.save(commit=False)  
                    profile.owner = x
                    if 'picture' in request.FILES:
                        profile.picture = request.FILES['picture']
                    profile.save()
                else:
                    print(profile_form.errors)
                registered = True
        else:
            print(user_form.errors)    
    else:
        user_form = UserForm()
        profile_form_set = formset_factory(UserProfileForm, max_num=5, extra=1)
        data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0' 
        }
        profile_form = profile_form_set(data)
        
    context_dict = {}
    context_dict['user_form'] = user_form
    context_dict['profile_form'] = profile_form
    context_dict['registered'] = registered
        
    return render(request, 'dogpark/register.html', context=context_dict)

@login_required
def people(request):
    u = request.user
    num_dogs = []
    my_list = []
    friends = Friendship.objects.filter(Q(from_friend=u) | Q(to_friend=u))
    friend_req = FriendRequest.objects.filter(Q(sender=u) | Q(receiver=u))
    user_list = User.objects.exclude(username=get_user(request))
    for x in friends.iterator():
        user_list = user_list.filter(~Q(id=x.from_friend.id) & ~Q(id=x.to_friend.id))
    for x in friend_req.iterator():
        user_list = user_list.filter(~Q(id=x.sender.id) & ~Q(id=x.receiver.id))
    for x in user_list:
        dog_list = Dog.objects.filter(owner=x)
        my_list.append((x, dog_list, len(dog_list)))
    context_dict = {}
    context_dict['my_list'] = my_list
    return render(request, 'dogpark/people.html', context=context_dict)

@login_required
def mypark(request):
    context_dict = {}
    u = request.user
    checked_in_friends = []
    visitors = None
    try:
        visitors = Owner.objects.exclude(user=request.user).filter(checked_in=True).count()
        current = Owner.objects.get(user=u)
        friends = Friendship.objects.filter(Q(from_friend = u) | Q(to_friend = u))
        for x in friends.iterator():
            if x.from_friend == u:
                ci_u = x.to_friend
            else:
                ci_u = x.from_friend
            if Owner.objects.get(Q(user=ci_u) & Q(checked_in=True)):
                checked_in_friends.append(ci_u)
    except Owner.DoesNotExist:
        print("Owner does not exist")
    if visitors == None:
        return render(request, 'dogpark/index.html', context=context_dict)
    context_dict['visitors'] = visitors
    context_dict['checked_in'] = current.checked_in
    context_dict['my_checked_in_friends'] = checked_in_friends
    return render(request, 'dogpark/mypark.html', context=context_dict)

@login_required
def park_events(request):
    if request.method == "GET":
        context_dict = {}
        try:
            events=Events.objects.all()
            context_dict['events'] = events
        except Events.DoesNotExist:
            events = None
        if events == None:
            return render(request, 'dogpark/mypark.html', context=context_dict)
        return render(request, 'dogpark/park_events.html', context=context_dict)
    else:
        return render(request, 'dogpark/mypark.html')

@login_required
def park_goals(request):
    context_dict = {}
    try:
        goals = Goals.objects.all()
        context_dict['goals'] = goals
    except Goals.DoesNotExist:
        goals = None
    if goals == None:
        return render(request, 'dogpark/mypark.html', context=context_dict)
    return render(request, 'dogpark/park_goals.html', context=context_dict)

@login_required
def attend_event(request):
    context_dict = {}
    elm_id = request.POST.get('eventid')
    data = {'response': -1}
    try:
        e = Events.objects.get(id=int(elm_id))
        e.attending = True 
        e.save()
    except Events.DoesNotExist:   
        e = None
    if e == None:
        return JsonResponse(data)
    return JsonResponse({'response': 1})
    
@login_required
def decline_event(request):
    context_dict = {}
    elm_id = request.POST.get('eventid')
    data = {'response': -1}
    try:
        e = Events.objects.get(id=int(elm_id))
        e.attending = False 
        e.save()
    except Events.DoesNotExist:
        e = None
    if e == None:
        return JsonResponse(data)
    return JsonResponse({'response': 1})
    
@login_required
def add_goal(request):
    context_dict = {}
    elm_id = request.POST.get('goalid')
    data = {'response': -1}
    try:
        e = Goals.objects.get(id=int(elm_id))
        e.add_goal = True 
        e.save()
    except Goals.DoesNotExist:
        e = None
    if e == None:
        return JsonResponse(data)
    return JsonResponse({'response': 1})    
    
@login_required
def remove_goal(request):
    context_dict = {}
    elm_id = request.POST.get('goalid')
    data = {'response': -1}
    try:
        e = Goals.objects.get(id=int(elm_id))
        e.add_goal = False 
        e.save()
    except Goals.DoesNotExist:
        e = None
    if e == None:
        return JsonResponse(data)
    return JsonResponse({'response': 1})
    
@login_required
def finish_goal(request):
    context_dict = {}
    elm_id = request.POST.get('goalid')
    data = {'response': -1}
    try:
        e = Goals.objects.get(id=int(elm_id))
        e.complete_goal = True
        e.points_earned = 50 
        e.save()
    except Goals.DoesNotExist:
        e = None
    if e == None:
        return JsonResponse(data)
    return JsonResponse({'response': 1})  
 
@login_required
def achievements(request):
    context_dict = {}
    total_points = 0
    try:
        g = Goals.objects.filter(complete_goal=True)
        if g.exists():
            for x in g.iterator():
                total_points = total_points + x.points_earned
                a = Achievement.objects.get_or_create(goal=x)[0]
                a.save()
        objs = Achievement.objects.all()
        context_dict['achievements'] = objs.order_by("created")
        context_dict['total_points'] = total_points
    except Achievement.DoesNotExist:
        objs = None
    if objs == None:
        return render(request, 'dogpark/index.html', context=context_dict)
    return render(request, 'dogpark/achievement.html', context=context_dict)

@login_required
def my_pet(request):
    context_dict = {}
    try:
        my_pets = Dog.objects.filter(owner_id=request.user.id)
    except Dog.DoesNotExist:
        my_pets = None
    context_dict['my_pets'] = my_pets
    if my_pets == None:
        return render(request, 'dogpark/index.html', context=context_dict)
    return render(request, 'dogpark/my_pet.html', context=context_dict)
        
class seeFriendRequests(View):
    @method_decorator(login_required)
    def get(self, request):
        context_dict = {}
        my_requests = None
        already_friends = None
        fr = True
        u = get_user(request)
        if not request.user.is_anonymous:
            try:
                already_friends = Friendship.objects.filter(Q(from_friend=u) | Q(to_friend=u))
                if not already_friends:
                    my_requests = FriendRequest.objects.filter(receiver=request.user)
                else:
                    for x in already_friends.iterator():
                        my_requests = FriendRequest.objects.filter(Q(receiver=request.user) & (~Q(sender_id=x.from_friend_id) | ~Q(sender_id=x.to_friend_id)))
            except ObjectDoesNotExist:
                try:
                    my_requests = FriendRequest.objects.filter(receiver=request.user)
                except ObjectDoesNotExist:
                    fr = None
                except FriendRequest.DoesNotExist:
                    fr = None
            if fr == None:
                request_exists = False
            else:
                request_exists = True
            context_dict['incoming_requests'] = my_requests
            context_dict['request_exists'] = request_exists
            return render(request, 'dogpark/see_friend_requests.html', context=context_dict)
    
class myFriends(View):
    @method_decorator(login_required)
    def get(self, request):
        context_dict = {}
        dog_list = []
        u = get_user(request)
        try:
            friendship = Friendship.objects.filter(Q(from_friend=u) | Q(to_friend=u))
            for friend in friendship:
                if friend.from_friend == u:
                    dog_list.append((Dog.objects.filter(owner=friend.to_friend), friend.to_friend))
                else:
                    dog_list.append((Dog.objects.filter(owner=friend.from_friend), friend.from_friend))
        except Friendship.DoesNotExist:
            friendship = None
        if friendship == None:
            return redirect(reverse('dogpark:index'))
        context_dict['friends'] = friendship
        context_dict['dogs'] = dog_list
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
        data = {'response': -1}
        uname = request.POST.get('uname')
        try:
            from_friend = request.user
            to_friend = User.objects.get(username=uname)
            friend, created = Friendship.objects.get_or_create(from_friend=from_friend, to_friend=to_friend)
            FriendRequest.objects.get(Q(sender=to_friend) & Q(receiver=from_friend)).delete()
            if created:
                return JsonResponse({'response': 1})
        except ValueError:
            return JsonResponse(data)
        return JsonResponse({'response': 1})
    
class check_in(View):
    @method_decorator(login_required)
    def post(self, request):
        try:
            obj = Owner.objects.get(user=request.user)
            obj.checked_in = True
            obj.save()
        except Owner.DoesNotExist:
            return JsonResponse({'response': -1})
        except ValueError:
            return JsonResponse({'response': -1})
        return JsonResponse({'response': 1})

class check_out(View):
    @method_decorator(login_required)
    def post(self, request):
        try:
            obj = Owner.objects.get(user=request.user)
            obj.checked_in = False
            obj.save()
        except Owner.DoesNotExist:
            return JsonResponse({'response': -1})
        except ValueError:
            return JsonResponse({'response': -1})
        return JsonResponse({'response': 1})
