'''
Created on Dec 13, 2016

@author: minbaev
'''
from django import forms
from django.contrib.auth.models import User
from rango.models import Category, Page, UserProfile

from registration.forms import RegistrationForm


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    
class UserProfileForm(forms.ModelForm):
    website=forms.URLField(label="Put your website", required=False)
    picture=forms.ImageField(label="Upload your picture", required=False)
    
    class Meta:
        model = UserProfile
        exclude = ('user',)


        
# class RegistrationFormEx(RegistrationForm):
#     website = forms.CharField(label = "Put your website:", required=False)
#     picture = forms.ImageField(label="Upload your picture", required=False)


    

class CategoryForm(forms.ModelForm):
#     name = forms.CharField(max_length=Category.MAX_LENGTH,
#                            help_text='Enter category name')
    name = forms.CharField(label="")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = Category
        fields = ('name',)
    
class PageForm(forms.ModelForm):
    title = forms.CharField(widget=forms.HiddenInput())
    url = forms.CharField(widget=forms.HiddenInput())
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    
    class Meta:
        model = Page
        exclude = ('category',)