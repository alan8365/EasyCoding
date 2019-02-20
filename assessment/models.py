from django.db import models
from account.models import User
from course.models import Course


# Create your models here.

class Content(models.Model):
    number = models.IntegerField()

    content = models.TextField(
        max_length=2100
    )

    isTitle = models.BooleanField(
        default=False
    )

    isText = models.BooleanField(
        default=False
    )

    isCode = models.BooleanField(
        default=False
    )

    isImage = models.BooleanField(
        default=False
    )

    isLink = models.BooleanField(
        default=False
    )

    isTable = models.BooleanField(
        default=False
    )

    assessment = models.ForeignKey(
        "Assessment",
        on_delete=models.CASCADE
    )

    def reset_type(self):
        self.isTitle = False
        self.isSubTitle = False
        self.isText = False
        self.isCode = False
        self.isImage = False
        self.isLink = False
        self.isTable = False

    def __str__(self):
        return "%s第%d段" % (str(self.assessment), self.number)

    def __ge__(self, other):
        if isinstance(other, Content):
            return self.number > other.number
        else:
            raise TypeError()


class Assessment(models.Model):
    title = models.CharField(
        max_length=50,
        null=True
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        null=True,
    )

    level = models.SmallIntegerField(
        default=1
    )

    def next_assessment(self):

        if self.course.lesson.number == 0:
            return Assessment.objects.get(pk=2)
        else:
            temp = list(Assessment.objects.filter(level=1, course__gt=self.course).exclude(course__lesson__number=0))
            temp.sort()

        try:
            return temp[0]
        except IndexError:
            return Assessment.complete_level_one_assessment()

    @staticmethod
    def complete_level_one_assessment():

        return Assessment.objects.get(pk=11)

    def __str__(self):
        if self.course.lesson.number == 100:
            return "%s" % self.title

        return "%d.%d %s" % (self.course.lesson.number, self.course.chapter, self.title)

    def __gt__(self, other):
        if isinstance(other, Assessment):
            if self.course == other.course:
                return self.level > other.level
            else:
                return self.course > other.course
        else:
            raise TypeError("Assessment can't compare with other type")

    def __ge__(self, other):

        return self > other or self == other


class AssessmentCode(models.Model):
    code = models.TextField(
        max_length=1500,
        null=True
    )

    user = models.ForeignKey(
        'account.User',
        on_delete=models.CASCADE,
        null=True,
    )

    ass = models.ForeignKey(
        'Assessment',
        on_delete=models.CASCADE,
        null=True,
    )

    # 投票數
    point = models.IntegerField(
        default=0
    )

    datetime = models.DateTimeField(
        auto_now_add=True,
        null=True
    )

    def __str__(self):
        return "%s的%s" % (str(self.user), str(self.ass))

    def __gt__(self, other):
        if isinstance(other, AssessmentCode):

            return self.ass > other.ass

        else:
            raise TypeError()

    class Meta:
        unique_together = ('ass', 'user')


class HaveVoted(models.Model):
    user = models.ForeignKey(
        'account.User',
        on_delete=models.CASCADE,
        null=True
    )

    ass_code = models.ForeignKey(
        'AssessmentCode',
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return "%s在%s投給%s" % (str(self.user), str(self.ass_code.ass), str(self.ass_code.user))


class Comment(models.Model):
    date = models.DateTimeField(
        auto_now_add=True
    )

    content = models.TextField(
        default=""
    )

    like = models.PositiveIntegerField(
        default=0
    )

    dislike = models.PositiveIntegerField(
        default=0
    )

    user = models.ForeignKey(
        'account.User',
        on_delete=models.CASCADE,
        null=True
    )

    ass_code = models.ForeignKey(
        'AssessmentCode',
        on_delete=models.CASCADE,
        null=True
    )

    reply = models.ForeignKey(
        'Comment',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return "%s comment in %s" % (str(self.user), str(self.ass_code))

    def save(self, *args, **kwargs):
        if not self.reply:
            self.reply = None

        super(Comment, self).save(*args, **kwargs)


class HaveLike(models.Model):
    is_like = models.BooleanField()

    user = models.ForeignKey(
        'account.User',
        on_delete=models.CASCADE,
        null=True
    )

    comment = models.ForeignKey(
        'Comment',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

# class HaveVoted(models.Model):
#     user = models.ForeignKey(
#         'account.User',
#         on_delete=models.CASCADE,
#         null=True
#     )
#
#     ass = models.ForeignKey(
#         'Assessment',
#         on_delete=models.CASCADE,
#         null=True
#     )
#
#     ass_code = models.ForeignKey(
#         'AssessmentCode',
#         on_delete=models.CASCADE,
#         null=True
#     )
#
#     def __str__(self):
#         return "%s在%s投給%s" % (str(self.user), str(self.ass_code.ass), str(self.ass_code.user))
