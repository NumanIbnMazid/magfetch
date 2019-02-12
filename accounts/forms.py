from allauth.account.forms import SignupForm
from django import forms
from django.conf import settings
from .models import UserProfile
import re

class CustomSignupForm(SignupForm):  
    def signup(self, request, user):
        user.save()
        userprofile, created = self.get_or_create(user=user)
        user.userprofile.save()

class UserForm(forms.ModelForm):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ('first_name', 'last_name')

class UserProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # magic 
        self.user = kwargs['instance'].user
        user_kwargs = kwargs.copy()
        user_kwargs['instance'] = self.user
        self.uf = UserForm(*args, **user_kwargs)
        # magic end 

        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)

        self.fields.update(self.uf.fields)
        self.initial.update(self.uf.initial)
        
        self.fields['first_name']   = forms.CharField(required=False,
            widget=forms.TextInput(attrs={'placeholder': 'Enter your first name'}))
        self.fields['last_name']    = forms.CharField(required=False,
            widget=forms.TextInput(attrs={'placeholder': 'Enter your last name'}))


    class Meta:
        model = UserProfile
        exclude = ['user', 'slug', 'image', 'user_type']

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if first_name != '' :
            allowed_char    = re.match(r'^[A-Za-z.,\- ]+$', first_name)
            length          = len(first_name)
            if length > 15:
                raise forms.ValidationError("Maximum 15 characters allowed !")
            if not allowed_char:
                raise forms.ValidationError("Please Enter Valid Name (Only Alpha values allowed, Ex:Abc) !")
        return first_name
    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if last_name != '' :
            allowed_char    = re.match(r'^[A-Za-z.,\- ]+$', last_name)
            length          = len(last_name)
            if length > 20:
                raise forms.ValidationError("Maximum 20 characters allowed !")
            if not allowed_char:
                raise forms.ValidationError("Please Enter Valid Name (Only Alpha values allowed, Ex:Abc) !")
        return last_name
        

    def save(self, *args, **kwargs):
        self.uf.save(*args, **kwargs)
        return super(UserProfileUpdateForm, self).save(*args, **kwargs)