from django import forms
from django.forms import ModelForm
from .models import News,CustomUser, OwnAnimal
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class NewsAddModelForm(ModelForm):
    class Meta():
        model = News
        fields = ["title", "content", "address", "mobile_phone", "main_image", "type"] 

class NewsChangeModelForm(ModelForm):
    class Meta():
        model = News
        fields = ["title", "content", "address", "mobile_phone", "main_image", "type", "status"] 

   


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)
    class Meta():
        model = CustomUser
        fields = [
            "username",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "email",
            "image",
            "phone"
        ]

class AnimalAddForm(ModelForm):
    class Meta():
        model = OwnAnimal
        fields = [
            "title",
            "content",
            "image"
        ]
