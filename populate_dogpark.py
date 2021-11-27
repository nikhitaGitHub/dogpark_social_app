import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','dogpark_social_app.settings')

import django
import datetime
django.setup()
from dogpark.models import Goals, Events, Owner, Dog, Friendship, FriendRequest
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.files import File

t1 = datetime.time(10, 33, 45)
t2 = datetime.time(11, 43, 55)
t3 = datetime.time(9, 00, 00)
t4 = datetime.time(18, 00, 00)

d1 = datetime.date(2021, 12, 10)
d2 = datetime.date(2021, 12, 1)
d3 = datetime.date(2021, 12, 5)
d4 = datetime.date(2021, 12, 7)
d5 = datetime.date(2021, 12, 15)
 

def populate():
    goals = [{'description': 'play fetch', 'points_earned': 50},
             {'description': 'play tug of war', 'points_earned': 50},
             {'description': 'play hide and seek', 'points_earned': 50},
             {'description': 'ride a bike', 'points_earned': 50},
             {'description': 'walk', 'points_earned': 50},
             {'description': 'hike', 'points_earned': 50},
             {'description': 'run', 'points_earned': 50}]
    
    events =[{'name': 'puppy play party' , 'date': d1, 'time': t1},
             {'name': 'charity event', 'date': d2, 'time': t2},
             {'name': 'foxhound get together' , 'date': d3, 'time': t3},
             {'name': 'labrador get together' , 'date': d4, 'time': t4},
             {'name': 'find friend event' , 'date': d5, 'time': t3},
             {'name': 'birthday party' , 'date': d5, 'time': t3},
             {'name': 'dog walk event' , 'date': d4, 'time': t4},
             {'name': 'find a playdate' , 'date': d5, 'time': t4}]
    
    dog_set_1 = [{'owner':None, 'breed': 205, 'breedname': 'Portuguese Water Dog', 'name': 'Sam', 'age': 1, 'gender': 'M', 'path': 'static/images/pwd.jfif', 'fname': 'pwd.jfif'}]
    
    dog_set_2 = [{'owner':None, 'breed': 85, 'breedname': 'Picardy Sheepdog', 'name': 'Cindrella', 'age': 7, 'gender': 'F', 'path': 'static/images/bg.jpg', 'fname': 'bg.jpg'}, 
                 {'owner':None, 'breed': 79, 'breedname': 'Maremma Sheepdog', 'name': 'Prince Charming', 'age': 8, 'gender': 'M', 'path': 'static/images/ms.jpg', 'fname': 'ms.jpg'}]
    
    dog_set_3 = [{'owner':None, 'breed': 74, 'breedname': 'Hungarian Pumi', 'name': 'Romeo', 'age': 15, 'gender': 'F', 'path': 'static/images/hp.jpg', 'fname': 'hp.jpg'}]
    
    dog_set_4 = [{'owner':None, 'breed': 63, 'breedname': 'Borzoi', 'name': 'Juliet', 'age': 10, 'gender': 'M', 'path': 'static/images/borzoi.jfif', 'fname': 'borzoi.jpg'}]
    
    dog_set_5 = [{'owner':None, 'breed': 78, 'breedname': 'Bearded Collie', 'name': 'Fuzzy', 'age': 3, 'gender': 'M', 'path': 'static/images/bc.jpg', 'fname': 'bc.jpg'},
                 {'owner':None, 'breed': 125,'breedname': 'French Bulldog', 'name': 'Wuzzy', 'age': 6, 'gender': 'F', 'path': 'static/images/bdog.jpg', 'fname': 'bdog.jpg'},
                 {'owner':None, 'breed': 124,'breedname': 'Schipperke', 'name': 'Buzzy', 'age': 8, 'gender': 'F', 'path': 'static/images/s.jpg', 'fname': 's.jpg'}]
    
    dog_set_6 = [{'owner':None, 'breed': 205, 'breedname': 'Portuguese Water Dog', 'name': 'Fido', 'age': 11, 'gender': 'M', 'path': 'static/images/pwd.jfif', 'fname': 'pwd.jfif'}]
    
    users = [{'username': 'Harry','password': '123','fname': 'Harry','lname': 'Potter', 'email': 'p@123.com', 'num': 1, 'dogs':dog_set_1, 'checked_in': False},
             {'username': 'Larry','password': '123','fname': 'Larry','lname': 'Shoeman', 'email': 's@123.com', 'num': 2, 'dogs':dog_set_2, 'checked_in': True},
             {'username': 'Marry','password': '123','fname': 'Marry','lname': 'Simpson', 'email': 'si@123.com', 'num': 1, 'dogs':dog_set_3, 'checked_in': True},
             {'username': 'Kenny','password': '123','fname': 'Kenny','lname': 'Rogers', 'email': 'r@123.com',  'num': 1, 'dogs':dog_set_4, 'checked_in': True},
             {'username': 'Penny','password': '123','fname': 'Penny','lname': 'Ackerman', 'email': 'a@123.com', 'num': 3, 'dogs':dog_set_5, 'checked_in': False},
             {'username': 'Denny','password': '123','fname': 'Denny','lname': 'heroku', 'email': 'd@123.com', 'num': 1, 'dogs': dog_set_6, 'checked_in': True}]
    
    for u in users:
        active_user = create_user(u['username'], u['password'], u['fname'], u['lname'], u['email'])
        create_owner(active_user, u['num'], u['dogs'], u['checked_in'])

    h =User.objects.get(username="Harry")
    l =User.objects.get(username="Larry")
    m =User.objects.get(username="Marry")
    d =User.objects.get(username="Denny")
    
    FriendRequest.objects.create(sender=m, receiver=h)
    FriendRequest.objects.create(sender=l, receiver=h)
    
    Friendship.objects.create(from_friend=h, to_friend=d)
    
    for item in goals:
        add_goal(item)
    
    for item in events:
        add_event(item)
    
def add_goal(item):
    g = Goals.objects.get_or_create(description=item['description'], points_earned=item['points_earned'])[0]
    g.save()

def add_event(item):
    e = Events.objects.get_or_create(name=item['name'], date=item['date'], time=item['time'])[0]
    e.save()
 
def create_dog(dog):
    created, __ = Dog.objects.get_or_create(owner=dog['owner'], breed=dog['breed'], breedname=dog['breedname'], name=dog['name'], age=dog['age'], gender=dog['gender'])
    created.picture.save(dog['fname'], File(open(dog['path'], 'rb')))
    created.save()
    
def create_owner(u, n, dog_info, val):
    created, __= Owner.objects.get_or_create(user=u, num_dogs=n, checked_in=val)
    if __:
        created.save()
        for i in range(n):
            dog_info[i]['owner'] = u
            create_dog(dog_info[i])
            
def create_user(username, password, fname, lname, email) :
    user = get_user_model().objects.create_user(username=username, first_name=fname, last_name=lname, email=email)
    user.set_password(password)
    user.save()
    return user
        
if __name__ == '__main__':
    print("Running populate dogpark")
    populate()