from django.db import models


# Create your models here.

class Wiki(models.Model):
    name = models.CharField(
        max_length=50
    )

    lesson = models.PositiveIntegerField()

    chapter = models.PositiveIntegerField()

    def __str__(self):
        if self.chapter == 0:
            return "%d.%s" % (self.lesson, self.name)
        else:
            return "%d.%d %s" % (self.lesson, self.chapter, self.name)

    def __repr__(self):
        return str(self)

    def __gt__(self, other):
        if isinstance(other, Wiki):
            if self.lesson > other.lesson:
                return True
            elif self.lesson < other.lesson:
                return False
            else:
                return self.chapter > other.chapter
        else:
            raise ValueError


class Content(models.Model):
    number = models.PositiveIntegerField(
        default=0
    )

    content = models.TextField(
        max_length=10000
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

    isTable = models.BooleanField(
        default=False
    )

    isImage = models.BooleanField(
        default=False
    )

    wiki = models.ForeignKey(
        'Wiki',
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return "%s NO.%d" % (str(self.wiki), self.number)

    def __gt__(self, other):
        if isinstance(other, Content):
            return self.number > other.number
        else:
            raise ValueError
