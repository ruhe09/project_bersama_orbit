from django.db import models
import hashlib
from django.utils import timezone
def _create_hash():
    hash = hashlib.sha1()
    hash.update(str(time.time()))
    return  hash.hexdigest()[:-10]

# Create your models here.
class Posting(models.Model):
    post_title = models.CharField(max_length=30)
    post_description = models.CharField(max_length=100)
    post_price = models.DecimalField(max_digits=9,decimal_places=0)
    post_text = models.TextField(blank=True)
    post_image = models.ImageField(upload_to="static/post_img/",null=True, blank=True)
    post_date = models.DateTimeField(auto_now_add=True, blank=True)
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
    user_updated = models.DateTimeField(auto_now_add=True)

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