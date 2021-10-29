import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','dogpark_social_app.settings')

import django
import datetime
django.setup()
from dogpark.models import Goals, Events

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
        
if __name__ == '__main__':
    print("Running populate dogpark")
    populate()