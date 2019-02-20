from django.contrib import admin
from .models import User, Achievement, Achievement_get
# Register your models here.

admin.site.register(User)
admin.site.register(Achievement)
admin.site.register(Achievement_get)