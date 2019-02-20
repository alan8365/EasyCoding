from django.shortcuts import render
from django.http.response import JsonResponse
from django.http import Http404
from django.contrib.auth.decorators import login_required

from .apps import CourseMenuContent, CourseAdmin, FillQuestion, compare_str
from .models import Course, Content, Fill_Answer, Lesson


# Create your views here.
@login_required
def course(request, lesson_number=-1, chapter=-1):
    user_course = request.user.course_progress

    if lesson_number == -1 and chapter == -1:
        lesson_number, chapter = user_course.lesson.number, user_course.chapter

    try:
        choice_course = Course.objects.get(lesson=lesson_number, chapter=chapter)
    except Course.DoesNotExist:
        if lesson_number < Lesson.get_lesson_length():
            chapter = 1
            lesson_number += 1
            choice_course = Course.objects.get(lesson=lesson_number, chapter=chapter)
        else:
            raise Http404("之後就沒囉!!")

    assessment_pk = False
    assessment_for_choice_course = choice_course.assessment_set.all().filter(level=1)

    if assessment_for_choice_course:
        assessment_pk = assessment_for_choice_course[0].pk

    if request.user.is_superuser:
        pass
    elif lesson_number > user_course.lesson.number:
        raise Http404("YOU SHALL NOT PASS!!!!")
    elif lesson_number == user_course.lesson.number:
        if chapter > user_course.chapter:
            raise Http404("YOU SHALL NOT PASS!!!!")

    if request.method == "GET":
        template = "course/course.html"

        all_content = list(Content.objects.filter(course=choice_course))
        all_content.sort()

        all_course_menu = []

        for i in Lesson.objects.all().exclude(number__gt=10).exclude(number__lt=1):
            all_course_menu.append(
                CourseMenuContent(i, user_course)
            )

        fill_question = FillQuestion(choice_course)

        return render(request, template, {"all_content": all_content,
                                          "course_name": str(choice_course),
                                          "all_course_menu": all_course_menu,
                                          "lesson": lesson_number,
                                          "chapter": chapter,
                                          "fill_question": fill_question,
                                          "assessment_pk": assessment_pk})

    user_answer = request.POST["answer"]
    fill_answers = Fill_Answer.objects.filter(fill__course=choice_course)

    is_answer_right = False
    which_false = [i for i in range(100)]

    for answer in fill_answers:

        is_answer_right, temp_which_false = compare_str(user_answer, answer.answer)

        if len(temp_which_false) < len(which_false):
            which_false = temp_which_false

        if is_answer_right:
            break

    is_assessment_exist = bool(assessment_pk)

    if is_answer_right:

        if choice_course == user_course and not is_assessment_exist:
            request.user.course_progress = choice_course.next_course()
            request.user.save()

    return JsonResponse({"is_answer_right": is_answer_right,
                         "which_false": which_false,
                         "is_assessment_exist": is_assessment_exist})


@login_required
def course_add(request, lesson_number=1, chapter=1):
    if not request.user.is_superuser:
        raise Http404("not exist")

    template = "course/seven.html"
    choice_course = Course.objects.get(lesson__number=lesson_number, chapter=chapter)

    if request.method == "GET":

        all_content = list(Content.objects.filter(course=choice_course))
        all_content.sort()

        all_course = []

        for i in Lesson.objects.all():
            all_course.append(
                CourseAdmin(i)
            )

        return render(request, template, {
            "all_content": all_content,
            "all_course": all_course,
            "lesson": lesson_number,
            "chapter": chapter
        })

    # data = request.POST.get("data[0][]")
    datas = dict(request.POST)
    number = int(datas["number"][0])
    size = len(choice_course.content_set.all())

    count = number if number > size else size

    for i in range(count):
        if i < number:
            data = datas["data[%d][]" % i]

            data_type = data[1]
            value = data[2]
        else:
            temp = Content.objects.get(course=choice_course, number=i)
            temp.delete()

            continue

        temp = Content.objects.get_or_create(course=choice_course, number=i)[0]

        temp.reset_type()

        if data_type == "text":
            temp.isText = True
        elif data_type == "code":
            temp.isCode = True
        elif data_type == "title":
            temp.isTitle = True
        elif data_type == "subtitle":
            temp.isSubTitle = True
        elif data_type == "image":
            temp.isImage = True
            if '/' in value:
                temp.content = value
            else:
                temp.content = "course_image/%d%d/%s" % (lesson_number, chapter, value)
            temp.save()
            continue

        temp.content = value

        temp.save()

    return JsonResponse({})
