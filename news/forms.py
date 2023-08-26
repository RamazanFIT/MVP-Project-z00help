from django import forms
from django.forms import ModelForm, Form
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

class ProfileChangeModelForm(ModelForm):
    class Meta():
        model = CustomUser
        fields = ["first_name", "last_name", "email", "image", "phone"] 

class ChangePasswordForm(Form):
    
    current_password = forms.CharField(widget=forms.PasswordInput())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())


class AnimalChangeModelForm(ModelForm):
    class Meta():
        model = OwnAnimal
        fields = ["image", "title", "content", "type"] 

   
