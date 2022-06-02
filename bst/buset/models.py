import hashlib

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser

def _create_hash():
    hash = hashlib.sha1()
    return  hash.hexdigest()[:-10]

User = settings.AUTH_USER_MODEL

class Posting(models.Model):
    user = models.ForeignKey(User,
                    default = 1,
                    null = True, 
                    on_delete = models.SET_NULL
                    )
    post_title = models.CharField(max_length=30)
    post_description = models.CharField(max_length=100)
    post_price = models.DecimalField(max_digits=9,decimal_places=0)
    post_text = models.TextField(blank=True)
    post_image = models.ImageField(upload_to="static/post_img/",null=True, blank=True)
    post_date = models.DateTimeField(auto_now_add=True, blank=True)
    post_date_modified = models.DateTimeField(auto_now=True, null=True)
    slug = models.SlugField(max_length=255,unique=True,null=False)
    def url(self):
        return reverse("article_detail", kwargs={"slug":self.slug})
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.post_title)
        return super().save(*args, **kwargs)


# class Users(AbstractUser):
#     first_name = models.CharField(max_length=16,null=True)
#     last_name = models.CharField(max_length=16,null=True)
#     password = models.CharField(max_length=30,default=_create_hash,unique=True)
#     email = models.EmailField()
#     image  = models.ImageField(upload_to="static")
#     role = models.CharField(max_length=6)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     phone = models.IntegerField(null=True)
#     username = models.CharField(max_length=16,unique=True,null=False,blank=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phonenumber = models.CharField(verbose_name="phone number", max_length=11)
    birthdate = models.DateField(verbose_name="birth date", null=True)
    image = models.ImageField(upload_to="static/users_img/",null=True, blank=True)
class Shop(models.Model):
    shop_name = models.CharField(max_length=30)
    shop_pp  = models.ImageField(upload_to="static")
    shop_created = models.DateTimeField(auto_now_add=True)
    shop_updated = models.DateTimeField(auto_now_add=True)    
  
class Cv_Model(models.Model):
    image = models.ImageField(_("image"), upload_to='images')

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        return str(os.path.split(self.image.path)[-1])