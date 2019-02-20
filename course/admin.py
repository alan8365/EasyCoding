from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Lesson)
admin.site.register(Course)
admin.site.register(Content)
admin.site.register(Fill)
admin.site.register(Fill_Answer)

