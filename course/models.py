from django.db import models


# Create your models here.

class Lesson(models.Model):
    number = models.IntegerField(
        primary_key=True
    )

    name = models.CharField(
        max_length=100
    )

    @staticmethod
    def get_lesson_length():
        return len(Lesson.objects.all())

    def next_lesson(self):

        result = Lesson.objects.get(number=self.number + 1)
        return result

    def __str__(self):
        return "%d.%s" % (self.number, self.name)

    def __gt__(self, other):
        if isinstance(other, Lesson):
            if other.number == 0:
                return False
            else:
                return self.number > other.number
        else:
            raise TypeError()

    def __ge__(self, other):
        return self > other or self == other

    def __lt__(self, other):
        if isinstance(other, Lesson):
            if other.number == 0:
                return False
            else:
                return self.number < other.number
        else:
            raise TypeError()

    def __add__(self, other):
        if isinstance(other, int):
            temp = self.number + other
            if temp > Lesson.get_lesson_length():
                return Lesson.objects.get(number=temp)
            else:
                raise ValueError("out of range")
        else:
            raise TypeError()


class Course(models.Model):
    name = models.CharField(
        max_length=100,
    )

    lesson = models.ForeignKey(
        "Lesson",
        on_delete=models.CASCADE
    )

    chapter = models.IntegerField(
        default=0
    )

    def __str__(self):
        if self.chapter == 0:
            return str(self.name)

        return "%d-%d %s" % (self.lesson.number, self.chapter, str(self.name))

    def __gt__(self, other):
        if isinstance(other, Course):
            if other.lesson.number == self.lesson.number == 0:
                return self.chapter > other.chapter
            elif other.lesson.number == 0:
                return False
            elif self.lesson.number == 0:
                return False

            if self.lesson > other.lesson:
                return True
            elif self.lesson < other.lesson:
                return False
            else:
                return self.chapter > other.chapter
        else:
            raise TypeError()

    def __ge__(self, other):
        return self > other or self == other

    def __lt__(self, other):
        if isinstance(other, Course):
            if other.lesson.number == 0:
                return False
            elif self.lesson.number == 0:
                return False

            if self.lesson < other.lesson:
                return True
            elif self.lesson > other.lesson:
                return False
            else:
                return self.chapter < other.chapter
        else:
            raise TypeError()

    # def __add__(self, other):
    #     if isinstance(other, int):
    #         if other == 1:
    #             try:
    #                 result = Course.objects.get(lesson=self.lesson, chapter=self.chapter+1)
    #                 return result
    #             except Course.DoesNotExist:
    #
    #                 lesson = self.lesson + 1
    #                 chapter = 1
    #
    #                 return Course.objects.get(lesson=lesson, chapter=chapter)
    #
    #     else:
    #         raise TypeError("%s is not allow" % type(other))

    def next_course(self):

        try:
            result = Course.objects.get(lesson=self.lesson, chapter=self.chapter + 1)
            return result

        except Course.DoesNotExist:

            try:
                lesson = self.lesson.next_lesson()
                chapter = 1

                return Course.objects.get(lesson=lesson, chapter=chapter)
            except Lesson.DoesNotExist:

                return Course.complete_course()

    @staticmethod
    def complete_course():

        return Course.objects.get(lesson__number=100, chapter=0)


class Content(models.Model):
    content = models.TextField(
        max_length=4000
    )

    number = models.IntegerField(
        default=-1
    )

    isTitle = models.BooleanField(
        default=False
    )

    isSubTitle = models.BooleanField(
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

    course = models.ForeignKey(
        "Course",
        on_delete=models.CASCADE,
        null=True
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
        return "%s第%d段" % (str(self.course), self.number)

    def __lt__(self, other):
        if isinstance(other, Content):
            return self.number < other.number

        return False


class Fill(models.Model):
    course = models.ForeignKey(
        "Course",
        on_delete=models.CASCADE
    )

    content = models.TextField(
        max_length=3000
    )

    question = models.TextField(
        max_length=3000,
        null=True
    )

    def __str__(self):
        return str(self.course)


class Fill_Answer(models.Model):
    answer = models.CharField(
        max_length=50
    )

    fill = models.ForeignKey(
        "Fill",
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return str(self.fill)
