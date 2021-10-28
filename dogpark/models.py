from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from dogpark.constants import charLen256, charLen100
import datetime

class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    num_dogs = models.IntegerField(default=0)
    def __str__(self):
        #return self.user.first_name + 
        return " is owner of " + self.num_dogs + " dogs"
    
class Dog(models.Model):
    GENDER_CHOICES = (
        ('F', 'Female'),
        ('M', 'Male'),
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    breed = models.CharField(max_length = charLen256) 
    name = models.CharField(max_length = charLen100)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    picture = models.ImageField(upload_to="dog_profile_picture", default="", blank=True)
    def __str__(self):
        return self.name + " is a " + self.breed + " and is " + str(self.age) + " years old."
    
class FriendRequest(models.Model):
    sender = models.ForeignKey(User, related_name='the_sender',on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='the_receiver', on_delete=models.CASCADE)
    def __str__(self):
        return "request sent"
    
    class Meta:
        unique_together = (('sender', 'receiver'),)
    
class Friendship(models.Model):
    from_friend = models.ForeignKey(User, related_name="from_friend", on_delete=models.CASCADE)
    to_friend= models.ForeignKey(User, related_name="to_friend", on_delete=models.CASCADE)
    def __str__(self):
        return "Friend request accepted"
    
    class Meta:
        unique_together = (('from_friend', 'to_friend'),)
        
class Events(models.Model):
    name = models.CharField(max_length=charLen256)
    date = models.DateField(default=datetime.date.today, blank=True, null=True)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    
class Goals(models.Model):
    description = models.CharField(max_length=charLen256)
    pointsEarned = models.IntegerField(default=0)