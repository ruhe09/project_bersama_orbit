from django.contrib import admin
from .models import Profile
from .models import Posting
admin.site.register(Posting)
admin.site.register(Profile)