import hashlib

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def _create_hash():
    hash = hashlib.sha1()
    hash.update(str(time.time()))
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
    post_slug = models.SlugField(max_length=255,unique=True,blank=True)
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    def __str__(self):
        return self.post_title

class Users(models.Model):
    user_name = models.CharField(max_length=30)
    user_password = models.CharField(max_length=16,default=_create_hash,unique=True)
    user_email = models.EmailField()
    user_pp  = models.ImageField(upload_to="static")
    user_role = models.CharField(max_length=6)
    user_created = models.DateTimeField(auto_now_add=True)
    user_updated = models.DateTimeField(auto_now=True)

class Shop(models.Model):
    shop_name = models.CharField(max_length=30)
    shop_pp  = models.ImageField(upload_to="static")
    shop_created = models.DateTimeField(auto_now_add=True)
    shop_updated = models.DateTimeField(auto_now_add=True)    
    
class Choice(models.Model):
    question = models.ForeignKey(Posting, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Cv_Model(models.Model):
    image = models.ImageField(_("image"), upload_to='images')

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        return str(os.path.split(self.image.path)[-1])