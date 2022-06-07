from unittest.util import _MAX_LENGTH
from buset.models import Posting
# from buset.models import Users
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from .models import Profile,Cv_Model, Bunga_Model


class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    # phone_number = forms.IntegerField(required=True)
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        # user.phone = self.cleaned_data['phone_number']
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['phonenumber']

class UserUpdtForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name")
        


class ProfileUpdtForm(forms.ModelForm):
    phonenumber = forms.IntegerField()
    #image = forms.ImageField()
    class Meta:
        model = Profile
        fields = ['phonenumber']
        #fields = ['image']
    
class ProfileImgUpdtForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class PostForm(forms.ModelForm):
    class Meta:
        model = Posting
        
        fields = ('post_title','post_description','post_price','post_text','post_image')

    


class Cv_Upload(forms.ModelForm):
    class Meta:
        model = Cv_Model
        fields = ['image']
        
class Bunga_Upload(forms.ModelForm):
    class Meta:
        model = Bunga_Model
        fields = ['image']

