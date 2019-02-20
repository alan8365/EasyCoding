from django.contrib import admin
from .models import *


class CommentAdmin(admin.ModelAdmin):
    fields = ('content', 'user', 'ass_code', 'reply')

    ordering = ('date',)


# Register your models here.
admin.site.register(Assessment)
admin.site.register(Content)
admin.site.register(AssessmentCode)
admin.site.register(HaveVoted)
admin.site.register(Comment, CommentAdmin)
