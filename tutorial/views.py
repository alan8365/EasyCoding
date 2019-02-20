import os

from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import loader

from EasyCoding.apps import assessment_list

from assessment.apps import execute_sql, get_vote_content_by_id, list_split, CommentContent
from assessment.models import Assessment, Comment, HaveLike, AssessmentCode, HaveVoted
from assessment.models import Content as assessment_Content
from assessment.codelib import function_data

from course.apps import CourseMenuContent, FillQuestion
from course.models import Lesson, Course
from course.models import Content as course_Content


@login_required
def home(request):
    template = "tutorial/home.html"

    if request.method == "GET":
        user_course = request.user.course_progress

        all_course = []

        for i in Lesson.objects.all().exclude(number__gt=11):
            all_course.append(
                CourseMenuContent(i, user_course)
            )

        assessment_level_completed = []

        for i in range(1, 6):
            sql = """
                SELECT COUNT(ac.id)
                FROM assessment_assessmentcode as ac, assessment_assessment as a 
                WHERE ac.user_id = %d and a.level = %d and ac.ass_id = a.id
            """ % (request.user.id, i)

            temp = execute_sql(sql)[0][0]

            assessment_level_completed.append(temp)

        temp = len(Assessment.objects.all()) - sum(assessment_level_completed)
        assessment_level_completed.append(temp)

        assessment_lists = [assessment_list(i, request.user) for i in
                            Lesson.objects.all().exclude(number__gt=11).exclude(number__lt=2)]

        return render(request, template, {'username': request.user.username,
                                          'user_course': user_course,
                                          'all_course': all_course,
                                          'assessment_level_completed': assessment_level_completed,
                                          'assessment_lists': assessment_lists,
                                          'domain': 'tutorial'})


@login_required
def course(request, lesson_number, chapter):
    user_course = request.user.course_progress

    lesson_number = 0

    if chapter < 1 or chapter > 2:
        raise Http404("YOU SHALL NOT PASS!!!!")

    choice_course = Course.objects.get(lesson=lesson_number, chapter=chapter)

    assessment_pk = False
    assessment_for_choice_course = choice_course.assessment_set.all().filter(level=1)

    if assessment_for_choice_course:
        assessment_pk = assessment_for_choice_course[0].pk

    if request.method == "GET":
        template = "tutorial/course.html"

        all_content = list(course_Content.objects.filter(course=choice_course))
        all_content.sort()

        all_course_menu = []

        for i in Lesson.objects.all().exclude(number=100):
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


@login_required
def assessment(request, pk):
    pk = 12

    template = 'tutorial/assessment.html'

    data = function_data[pk]
    path = 'assessment/code/' + request.user.username
    user_file = path + '/' + str(data) + '.py'

    choice_assessment = Assessment.objects.get(pk=pk)

    # GET
    if request.method == 'GET':

        code = ''

        # 如果路徑上有檔案則輸入至code，否則輸入預設
        if os.path.isfile(user_file):
            with open(user_file, 'r') as f:
                temp = f.readlines()

                for i in temp:
                    code += i
        else:
            code = "def %s%s:" % (data.function_name, data.function_input)

        all_content = assessment_Content.objects.filter(assessment_id=pk)

        return render(request, template,
                      {'ass': choice_assessment,
                       'all_content': all_content,
                       'org_code': "def %s%s:" % (data.function_name, data.function_input),
                       'code': code,
                       'user': request.user.nickName,
                       'pk': pk})


@login_required
def vote(request, pk, sort_by="vote_number", page=1):
    template = "tutorial/vote.html"
    pk = 12

    if request.method == "GET":
        ass = Assessment.objects.get(pk=pk)

        contents = get_vote_content_by_id(pk, request.user.id)

        sort_types = {
            "vote_number": "票數較多",
            "date_first": "由新至舊",
            "date_last": "由舊至新"
        }

        if sort_by == "vote_number":
            contents = sorted(contents, key=lambda x: x.point_percent, reverse=True)
        elif sort_by == "date_first":
            contents = sorted(contents, key=lambda x: x.datetime, reverse=True)
        elif sort_by == "date_last":
            contents = sorted(contents, key=lambda x: x.datetime)

        contents = list_split(contents, 4)
        page_number = len(contents)

        sql = """
            select ass_code_id
            from assessment_havevoted as hv, assessment_assessmentcode as ac
            where hv.user_id = %d and ac.ass_id = %d and hv.ass_code_id = ac.id    
        """ % (request.user.id, pk)

        already_voted = execute_sql(sql)
        already_voted = already_voted[0][0] if already_voted else None

        return render(request, template,
                      {"assessment": ass,
                       "contents": contents[page - 1],
                       "pk": pk,
                       "already_voted_id": already_voted,
                       "sort_by": sort_by,
                       "sort_types": sort_types.items(),
                       "page": page,
                       "page_number": page_number,
                       })
