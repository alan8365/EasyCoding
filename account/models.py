from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# Create your models here.
class User(AbstractUser):
    nickName = models.CharField(
        _('用戶名'),
        max_length=128,
        unique=True,
        error_messages={
            'unique': _("已經有人用過囉囉囉"),
        }
    )

    email = models.EmailField(
        _('電子信箱'),
        unique=True,
    )

    vote_number = models.PositiveIntegerField(
        _('投票數'),
        default=0
    )

    image_url = models.TextField(
        default="media/user_images/default/bug.png"
    )

    is_commentable = models.BooleanField(
        default=False
    )

    course_progress = models.ForeignKey(
        "course.Course",
        on_delete=models.CASCADE,
        null=True,
    )

    assess_progress = models.ForeignKey(
        "assessment.Assessment",
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return self.nickName


class Achievement(models.Model):
    name = models.CharField(
        primary_key=True,
        max_length=100
    )

    title = models.CharField(
        max_length=100
    )

    description = models.TextField(
        max_length=1000
    )

    image = models.CharField(
        max_length=100
    )

    level = models.IntegerField(
        default=0
    )

    def __str__(self):
        return self.title

    def __gt__(self, other):
        if isinstance(other, Achievement):

            return self.level > other.level
        else:

            raise TypeError()

    def __lt__(self, other):
        if isinstance(other, Achievement):

            return self.level < other.level
        else:

            raise TypeError()


class Achievement_get(models.Model):
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE
    )

    achievement = models.ForeignKey(
        "Achievement",
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return "%s解鎖了%s" % (str(self.user), str(self.achievement))
