from django import forms
from django.contrib.auth.models import User
from django.template.defaultfilters import first
from dogpark.constants import charLen256, charLen100
from dogpark.models import Dog, Owner

#Present user to save 5 dogs at the time of registeration
DOG_NUMBER_CHOICES=[(1,1), (2,2), (3,3), (4,4), (5,5)]

#Form to store User information like email , password, number of dogs and full name
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=True),
    first_name = forms.CharField(max_length=charLen100, widget = forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=charLen100, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    num_dogs = forms.CharField(label="How many dogs do you own?", widget=forms.Select(choices=DOG_NUMBER_CHOICES, attrs={'class': "custom-select"}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password','first_name', 'last_name', 'num_dogs')

#Form to store each of their dogs information
class UserProfileForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=Dog.GENDER_CHOICES, widget=forms.Select(attrs={'class': "custom-select"}))
    age = forms.NumberInput(attrs={'required':True})
    breed = forms.ChoiceField(choices=Dog.BREED_CHOICES, widget=forms.Select(attrs={'class': "custom-select"}))
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'dog\'s name'}))
    class Meta:
        model = Dog
        fields = ('gender', 'age', 'breed', 'name', 'picture') 