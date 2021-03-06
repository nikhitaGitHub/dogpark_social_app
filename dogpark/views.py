from re import U
from django.core.exceptions import ObjectDoesNotExist
from django.forms.formsets import formset_factory
from django.forms.widgets import PasswordInput
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from dogpark.models import Friendship, Owner, Dog, FriendRequest, Goals, MyGoal, Events, MyEvents, Achievement, Ratings
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
from django.utils import timezone

in_proximity_detected = False

#helper function to find list of friendsly only who are checked in
def find_checked_in_friends(u):
    checked_in_friends = []
    #fetch from DB filetering results
    friends = Friendship.objects.filter(Q(from_friend = u) | Q(to_friend = u))
    for x in friends.iterator():
        if x.from_friend == u:
            ci_u = x.to_friend
        else:
            ci_u = x.from_friend
        try:
            # Query DB to fetch a value using Complex queries
            if Owner.objects.get(Q(user=ci_u) & Q(checked_in=True)):
                checked_in_friends.append(ci_u)
        except Owner.DoesNotExist:
            pass
    return checked_in_friends
        
#Helper function 
def helper_index(request):
    u = request.user
    context_dict = {}
    checked_in_friends = find_checked_in_friends(u)
    try:
        # Fetch everything but the current user
        visitors = Owner.objects.exclude(user=u).filter(checked_in=True).count()
    except:
        visitors = 0  
    context_dict["visitors"] = visitors     
    context_dict["my_checked_in_friends"] = checked_in_friends
    context_dict["u"] = u
    return context_dict 

# to handle HP2 on proximity to park, executes upon location chagnge
def render_near_park(request):
    context_dict = {}
    u = request.user
    try:
        current = Owner.objects.get(user=u)
        context_dict['checked_in'] = current.checked_in
    except:
        context_dict['checked_in'] = False
    return render(request, 'dogpark/index_close.html', context=context_dict)

#Same executes upon POST request 
def index_close(request):
    global in_proximity_detected
    close = request.POST.get('in_proximity')
    if(close == "1" and in_proximity_detected == False):
        in_proximity_detected = True
        return HttpResponse(1)
    elif(close == "0" and in_proximity_detected == True):
        in_proximity_detected = False
        return HttpResponse(1)
    return HttpResponse(0)

#HP1 when user is at home
def index(request):
    global in_proximity_detected
    context_dict = {}
    checked_in_friends = []
    u = request.user
    #Variable to detect if user is still close to the park
    if in_proximity_detected == True:
        return redirect(reverse('dogpark:render_near_park'))
    if not request.user.is_anonymous:
        in_proximity_detected = False
        context_dict = helper_index(request)
    return render(request, 'dogpark/index.html', context=context_dict)

#Logs a user in, HttpResponse for error handling
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
 
#logs a user out
@login_required   
def user_logout(request):
    logout(request)
    #re route to the homepage upon success
    return redirect(reverse('dogpark:index'))

#Fetch as many forms as the number of dogs
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

#User Registeration into Dog and Owner Model 
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
                    profile.breedname = profile.get_breed_display()
                    for k in request.FILES.keys():
                        if k.endswith('picture'):
                            profile.picture = request.FILES[k]
                            profile.save()
                registered = True
            else:
                print(profile_form.errors)
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

#Decorator mandating login
@login_required
# Find active users to view and potenitally friend
def people(request):
    u = request.user
    num_dogs = []
    my_list = []
    # Do not fetch current friends of the user
    friends = Friendship.objects.filter(Q(from_friend=u) | Q(to_friend=u))
    #Do not fetch current active freind requests with the user
    friend_req = FriendRequest.objects.filter(Q(sender=u) | Q(receiver=u))
    user_list = User.objects.exclude(username=get_user(request))
    # Iterate over all querys fetched so far
    for x in friends.iterator():
        #Fruther filter out those with whom user already has a freind request active
        user_list = user_list.filter(~Q(id=x.from_friend.id) & ~Q(id=x.to_friend.id))
    for x in friend_req.iterator():
        user_list = user_list.filter(~Q(id=x.sender.id) & ~Q(id=x.receiver.id))
    for x in user_list:
        #Fetch pet details of the current user 
        dog_list = Dog.objects.filter(owner=x)
        my_list.append((x, dog_list, len(dog_list)))
    context_dict = {}
    #Display dog details of every user on the UI
    context_dict['my_list'] = my_list
    return render(request, 'dogpark/people.html', context=context_dict)

#Render my park information , GET request
@login_required
def mypark(request):
    return render(request, 'dogpark/mypark.html')

#Fetch my pet information and display, simple GET request
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

class park_events(View):
    #Decorator specifying login is mandatory for this to execute
    @method_decorator(login_required)
    #Fetch the park events in DB to display, just a View request
    def get(self, request):
        context_dict = {}
        eventslist = []
        try:
            events=Events.objects.all()
            #Find the events user intends to attend and filter them to display as 'attending'
            myevents = MyEvents.objects.filter(owner=request.user)
            for x in myevents.iterator():
                eventslist.append(getattr(x, 'myevent'))
            context_dict['events'] = events
            context_dict['myevents'] = eventslist
        except Events.DoesNotExist:
            events = None
        if events == None:
            return render(request, 'dogpark/index_close.html', context=context_dict)
        return render(request, 'dogpark/park_events.html', context=context_dict)

#Decorator specifying login is mandatory for this to execute
@login_required
def park_goals(request):
    context_dict = {}
    mygoals = []
    my_achievements = []
    try:
        goals = Goals.objects.all()
        mygoal = MyGoal.objects.filter(owner=request.user)
        for x in mygoal.iterator():
            mygoals.append(getattr(x, 'goal'))   
        a = Achievement.objects.filter(owner=request.user)
        for x in a:
            #Fetch achievements and reset to display
            my_achievements.append(getattr(x, 'goal'))
        context_dict['goals'] = goals
        context_dict['mygoal']  = mygoals
        context_dict['completed'] = my_achievements
    except Goals.DoesNotExist:
        goals = None
    if goals == None:
        return render(request, 'dogpark/index_close.html', context=context_dict)
    return render(request, 'dogpark/park_goals.html', context=context_dict)

#Add an event to the attending list
@login_required
def attend_event(request):
    context_dict = {}
    elm_id = request.POST.get('eventid')
    data = {'response': -1}
    try:
        e = Events.objects.get(id=int(elm_id))
        me = MyEvents.objects.get_or_create(myevent=e, owner=request.user)[0]
    except Events.DoesNotExist or ValueError:   
        e = None
        me = None
    if e == None or me == None:
        return JsonResponse(data)
    return JsonResponse({'response': 1})

#Delete and event from the attendind list
@login_required
def decline_event(request):
    context_dict = {}
    elm_id = request.POST.get('eventid')
    data = {'response': -1}
    try:
        e = Events.objects.get(id=int(elm_id))
        me = MyEvents.objects.get(myevent= e, owner= request.user) 
        me.delete()
    except Events.DoesNotExist:
        e = None
    if e == None:
        return JsonResponse(data)
    return JsonResponse({'response': 1})

#Add a goal to start
@login_required
def add_goal(request):
    context_dict = {}
    elm_id = request.POST.get('goalid')
    data = {'response': -1}
    try:
        e = Goals.objects.get(id=int(elm_id))
        MyGoal.objects.create(goal=e, owner=request.user)
    except Goals.DoesNotExist:
        e = None
    if e == None:
        return JsonResponse(data)
    return JsonResponse({'response': 1})    

#Remove a gaol from list of goals to undertake
@login_required
def remove_goal(request):
    context_dict = {}
    elm_id = request.POST.get('goalid')
    data = {'response': -1}
    try:
        e = Goals.objects.get(id=int(elm_id))
        MyGoal.objects.get(goal=e, owner=request.user).delete()
        e.save()
    except Goals.DoesNotExist:
        e = None
    if e == None:
        return JsonResponse(data)
    return JsonResponse({'response': 1})

#Store user provided rating
@login_required
def rating(request):
    rating = request.POST.get('rating')
    data = {'response': -1}
    try:
        Ratings.objects.create(rating=rating, owner=request.user)
    except Ratings.DoesNotExist:
        print("DB no exist")        
    return JsonResponse({'response': 1})

#Mark a goal finished hence, adding to achievment
@login_required
def finish_goal(request):
    context_dict = {}
    elm_id = request.POST.get('goalid')
    data = {'response': -1}
    try:
        e = Goals.objects.get(id=int(elm_id))
        a = Achievement.objects.create(goal=e, owner=request.user)
        MyGoal.objects.get(goal=e, owner=request.user).delete()
    except Goals.DoesNotExist:
        e = None
    if e == None:
        return JsonResponse(data)
    return JsonResponse({'response': 1})  

#Store a list of all completed goals with date to store history and pointes earned
@login_required
def achievements(request):
    context_dict = {}
    total_points = 0
    try:
        a = Achievement.objects.filter(owner=request.user)
        if a.exists():
            for x in a.iterator():
                total_points = total_points + x.goal.points_earned
        context_dict['achievements'] = a.order_by("created")
        context_dict['total_points'] = total_points
    except Achievement.DoesNotExist:
        a = None
    if a == None:
        return render(request, 'dogpark/index.html', context=context_dict)
    return render(request, 'dogpark/achievement.html', context=context_dict)
        
# Has method to view all received or active friend requests
class seeFriendRequests(View):
    @method_decorator(login_required)
    def get(self, request):
        context_dict = {}
        my_requests = None
        already_friends = None
        my_list = []
        fr = True
        u = get_user(request)
        if not request.user.is_anonymous:
            try:
                already_friends = Friendship.objects.filter(Q(from_friend=u) | Q(to_friend=u))
                if not already_friends:
                    my_requests = FriendRequest.objects.filter(receiver=request.user)
                else:
                    #If the user is already friends now with them, either remove from friend request table or do not fetch to show
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
                for x in my_requests:
                    dog_list = Dog.objects.filter(owner=x.sender)
                    my_list.append((x, dog_list, len(dog_list)))
            context_dict['incoming_requests'] = my_list
            context_dict['request_exists'] = request_exists
            return render(request, 'dogpark/see_friend_requests.html', context=context_dict)

#Holds list of all friends to display
class myFriends(View):
    @method_decorator(login_required)
    def get(self, request):
        context_dict = {}
        dog_list = []
        u = get_user(request)
        try:
            #Freindship can be 2 way, so show both
            friendship = Friendship.objects.filter(Q(from_friend=u) | Q(to_friend=u))
            for friend in friendship:
                if friend.from_friend == u:
                    #retrive corresponding friend's dog details
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

#store in thd DB sent friend request
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

#Store ACcepted freind requests taht is friend a person    
class AcceptRequests(View):
    @method_decorator(login_required)
    def post(self,request):
        data = {'response': -1}
        uname = request.POST.get('uname')
        try:
            from_friend = request.user
            to_friend = User.objects.get(username=uname)
            friend, created = Friendship.objects.get_or_create(from_friend=from_friend, to_friend=to_friend)
            #Since accepted so delete from friend reqeust table
            FriendRequest.objects.get(Q(sender=to_friend) & Q(receiver=from_friend)).delete()
            if created:
                return JsonResponse({'response': 1})
        except ValueError:
            return JsonResponse(data)
        return JsonResponse({'response': 1})
    
# Check in a user by setting checked in attribute to true
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

#Check out a user by setting checked in attribute to false
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
