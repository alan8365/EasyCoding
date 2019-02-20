from django.apps import AppConfig
from .models import Course, Fill, Fill_Answer


class CourseConfig(AppConfig):
    name = 'course'


class CourseMenuContent:

    def __init__(self, lesson, user_course):

        self.lesson = lesson
        self.courses = list(Course.objects.filter(lesson__number=lesson.number))
        self.courses.sort()

        self.lesson_progress = user_course.lesson
        self.chapter_progress = user_course.chapter

        self.is_done = False
        self.is_lock = False

        if user_course.lesson < lesson:
            self.is_lock = True

            for course in self.courses:
                course.is_lock = True
                course.is_done = False

        elif user_course.lesson > lesson:
            self.is_done = True

            for course in self.courses:
                course.is_lock = False
                course.is_done = True

        else:

            for course in self.courses:
                if course > user_course:
                    course.is_lock = True
                    course.is_done = False
                elif course < user_course:
                    course.is_lock = False
                    course.is_done = True
                else:
                    course.is_lock = False
                    course.is_done = False


class CourseAdmin:

    def __init__(self, lesson):
        self.lesson = lesson
        self.data = list(Course.objects.filter(lesson__number=lesson.number))
        self.data.sort()


class FillQuestion:

    def __init__(self, course):
        fill_question = Fill.objects.get(course=course)

        self.content = fill_question.content
        self.question = change_fillquestion(fill_question.question)


def change_fillquestion(s):
    if isinstance(s, str):
        temp = """<input type="text" name="answer" maxlength="1" size="1" class="default">"""

        s = s.replace("@_@", temp)

        return s
    else:
        raise TypeError()


def compare_str(str1, str2):
    print("str1:%s" % str1)
    print("str2:%s" % str2)

    is_equal = True
    which_false = []

    for i in range(len(str1)):

        if str1[i] != str2[i]:
            is_equal = False

            which_false.append(i)

    print(which_false)

    return is_equal, which_false
