from django.http import JsonResponse
from django.shortcuts import render, redirect

from .apps import assessment_list
from wiki.apps import clean_table_content, clean_sql_content
from course.apps import CourseMenuContent
from course.models import Lesson
from assessment.apps import execute_sql
from assessment.models import Assessment


def home(request):
    if not request.user.is_authenticated:
        return redirect('account:index')

    if request.user.course_progress.lesson.number == 0:
        return redirect('tutorial:home')

    if request.method == "GET":
        user_course = request.user.course_progress

        all_course = []

        for i in Lesson.objects.all().exclude(number__gt=11).exclude(number__lt=1):
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

        temp = len(Assessment.objects.all()) - sum(assessment_level_completed) - 1
        assessment_level_completed.append(temp)

        assessment_lists = [assessment_list(i, request.user) for i in
                            Lesson.objects.all().exclude(number__gt=11).exclude(number__lt=2)]

        return render(request, 'home.html', {'username': request.user.username,
                                             'user_course': user_course,
                                             'all_course': all_course,
                                             'assessment_level_completed': assessment_level_completed,
                                             'assessment_lists': assessment_lists,
                                             'domain': 'course'})

    search = request.POST['search']
    search_highlight = "<highlight>%s</highlight>" % search
    search_for_sql = '@' + '@'.join(search)

    sql = """
        SELECT lesson, chapter, `name`
        FROM wiki_wiki 
        WHERE chapter != 0 AND `name` LIKE "%%%s%%"
        ESCAPE "@"
        """ % search_for_sql

    search_title_result = execute_sql(sql)
    search_title_result = ((i[0], i[1], i[2].replace(search, search_highlight)) for i in search_title_result)

    sql = """
        SELECT w.lesson, w.chapter, w.name, c.content
        FROM wiki_content as c, wiki_wiki as w
        WHERE (c.isText = 1 OR c.isTitle = 1) AND c.wiki_id = w.id AND c.content LIKE "%%%s%%"
        ESCAPE "@"
        """ % search_for_sql

    search_content_result = execute_sql(sql)
    search_content_result = clean_sql_content(search_content_result, search)
    # search_content_result = ((i[0], i[1], i[2], i[3].replace(search, search_highlight)) for i in search_content_result)

    sql = '''
        select w.lesson, w.chapter, w.name, c.content
        from wiki_content as c, wiki_wiki as w 
        where isTable = 1 and c.wiki_id = w.id
        '''

    search_table_result = execute_sql(sql)
    search_table_result = ((i[0], i[1], i[2], clean_table_content(i[3])) for i in search_table_result)
    search_table_result = (i for i in search_table_result if i[3].find(search) != -1)
    search_table_result = clean_sql_content(search_table_result, search)
    # search_table_result = ((i[0], i[1], i[2], i[3].replace(search, search_highlight)) for i in search_table_result)

    search_content_result = tuple(search_content_result) + tuple(search_table_result)

    return JsonResponse(
        {"search_title_result": tuple(search_title_result),
         "search_content_result": search_content_result})
