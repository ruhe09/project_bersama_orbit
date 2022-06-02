from buset.models import Posting
# from buset.models import Users
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from .models import Profile,Cv_Model


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

class PostForm(forms.ModelForm):
    class Meta:
        model = Posting
        
        fields = ('post_title','post_description','post_price','post_text','post_image')
        
    # post_title = models.CharField(max_length=30)
    # post_description = models.CharField(max_length=100)
    # post_price = models.DecimalField(max_digits=9,decimal_places=0)
    # post_text = models.TextField()
    # post_image = models.ImageField(upload_to="static")
    # post_date = models.DateTimeField(auto_now_add=True)
    


class Cv_Upload(forms.ModelForm):
    class Meta:
        model = Cv_Model
        fields = ['image']
