from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.template import loader
from django.contrib.auth.decorators import login_required

from EasyCoding.apps import assessment_list
from course.models import Lesson
from .check import function_data, check_user_code, usercode_handler
from .models import Assessment, AssessmentCode, HaveVoted, Comment, HaveLike, Content
from .apps import execute_sql, update_assess_code, get_vote_content_by_id, CommentContent, list_split

import os
import signal
import sys
from traceback import extract_tb
from random import randint


# Create your views here.
@login_required
def assessment(request, pk=-1):
    if pk == -1:
        pk = request.user.assess_progress.id
    if pk == 11:
        sql = """
            select id
            from assessment_assessment
            where id not in (
                        select a.id
                        from assessment_assessment as a,
                             assessment_assessmentcode as ac
                        where ac.user_id = 6
                          and ac.ass_id = a.id);
        """

        have_not_complete_assessment = execute_sql(sql)

        if have_not_complete_assessment:
            temp = randint(0, len(have_not_complete_assessment) - 1)
            pk = have_not_complete_assessment[temp][0]
        else:
            pk = 20  # TODO knacpack ppp

    template = 'assessment/assessment.html'

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

        all_content = Content.objects.filter(assessment_id=pk)

        return render(request, template,
                      {'ass': choice_assessment,
                       'all_content': all_content,
                       'org_code': "def %s%s:" % (data.function_name, data.function_input),
                       'code': code,
                       'user': request.user.nickName,
                       'pk': pk})

    # POST

    code = request.POST.get('code')

    # 如果沒有code就罵他
    if not code:
        messages.error(request, "打code進來啦")
        return render(request, template)

    if function_data[pk].function_name not in code:
        output = "請不要亂改函式名稱"

        response = JsonResponse({'output': output, "is_answer_right": False}, safe=False)
        return response

    # 如果沒有資料夾就創一個
    if not os.path.isdir(path):
        os.mkdir(path)

    with open(user_file, 'w') as f:
        f.write(code)

    signal.signal(signal.SIGALRM, usercode_handler)
    signal.alarm(5)
    print(code)

    is_answer_right = False

    try:
        is_answer_right, output = check_user_code(pk, code)
    except SyntaxError as e:
        exc_type, exc_value, exc_tb = sys.exc_info()
        line_number = exc_value.lineno

        output = "在第%d行發生語法錯誤" % line_number

    except BaseException as e:
        print(e)
        is_answer_right = False
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(extract_tb(exc_tb))
        temp = extract_tb(exc_tb)[-1]
        output = "在第%d行發生錯誤：\n%s" % (temp.lineno, str(exc_value))

    if "submit" in request.POST and is_answer_right:
        update_assess_code(request.user.id, pk, code)

        course_for_assessment = choice_assessment.course

        if course_for_assessment >= request.user.course_progress:
            request.user.course_progress = course_for_assessment.next_course()

        if choice_assessment >= request.user.assess_progress:
            request.user.assess_progress = request.user.assess_progress.next_assessment()

        request.user.save()

    response = JsonResponse({'output': output, "is_answer_right": is_answer_right}, safe=False)
    return response


@login_required
def vote(request, pk, sort_by="vote_number", page=1):
    template = "assessment/vote.html"
    user = request.user

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

    # POST

    post_type = request.POST['type']

    if post_type == 'like':

        comment_id = request.POST['id']

        sql = """
            select is_like, id
            from assessment_havelike
            where user_id = %d and comment_id = %s
        """ % (request.user.id, comment_id)

        last_like = execute_sql(sql)
        comment = Comment.objects.get(pk=comment_id)

        if not last_like:
            comment.like += 1
            comment.save()

            HaveLike.objects.create(
                is_like=True,
                user_id=request.user.id,
                comment_id=comment_id
            )

            status = 'create'

        elif last_like[0][0]:
            comment.like -= 1
            comment.save()

            temp = HaveLike.objects.get(pk=last_like[0][1])
            temp.delete()

            status = 'delete'

        else:
            comment.like += 1
            comment.dislike -= 1
            comment.save()

            temp = HaveLike.objects.get(pk=last_like[0][1])
            temp.is_like = True
            temp.save()

            status = 'change'

        response = JsonResponse({"status": status, "like": comment.like, "dislike": comment.dislike})

    elif post_type == 'dislike':

        comment_id = request.POST['id']

        sql = """
            select is_like, id
            from assessment_havelike
            where user_id = %d and comment_id = %s
        """ % (request.user.id, comment_id)

        last_like = execute_sql(sql)
        comment = Comment.objects.get(pk=comment_id)

        if not last_like:
            comment.dislike += 1
            comment.save()

            HaveLike.objects.create(
                is_like=False,
                user_id=request.user.id,
                comment_id=comment_id
            )

            status = "create"

        elif last_like[0][0]:
            comment.dislike += 1
            comment.like -= 1
            comment.save()

            temp = HaveLike.objects.get(pk=last_like[0][1])
            temp.is_like = False
            temp.save()

            status = "change"

        else:
            comment.dislike -= 1
            comment.save()

            temp = HaveLike.objects.get(pk=last_like[0][1])
            temp.delete()

            status = "delete"

        response = JsonResponse({"status": status, "like": comment.like, "dislike": comment.dislike})

    elif post_type == "comment":

        ass_code_id = int(request.POST.get("ac_id"))
        reply_id = request.POST.get("reply")
        reply_id = int(reply_id) if reply_id != "None" else None
        content = request.POST.get("content")

        return_comment = Comment.objects.create(
            content=content,
            user_id=request.user.id,
            ass_code_id=ass_code_id,
            reply_id=reply_id
        )

        if reply_id:

            t = loader.get_template('assessment/vote-comment-reply.html')

            b = CommentContent(return_comment, read_user_id=request.user.id)

            c = t.render({
                'user': request.user,
                'replied': b
            })

        else:

            t = loader.get_template('assessment/vote-comment.html')

            b = CommentContent(return_comment, read_user_id=request.user.id)

            c = t.render({
                'content': {"id": ass_code_id},
                'user': request.user,
                'main_comment': b
            })

        response = JsonResponse({"new_comment": c})

    elif post_type == "vote":
        org_point = -1
        org_id = 0

        ass_code_id = int(request.POST.get("id"))
        ass_id = pk

        have_vote_this_ass_code = HaveVoted.objects.filter(user_id=user.id, ass_code_id=ass_code_id)

        if have_vote_this_ass_code:

            HaveVoted.objects.get(pk=have_vote_this_ass_code[0].pk).delete()
            ass_code = AssessmentCode.objects.get(pk=ass_code_id)
            ass_code.point -= 1
            ass_code.save()
            point = ass_code.point
            org_id = ass_code_id

        else:

            have_vote_this_ass = HaveVoted.objects.filter(user_id=request.user.id,
                                                          ass_code__ass_id=ass_id)

            if have_vote_this_ass:

                have_not_update_ass_code = AssessmentCode.objects.filter(pk=have_vote_this_ass[0].ass_code_id)

                if have_not_update_ass_code:
                    org_ass_code = AssessmentCode.objects.get(id=have_vote_this_ass[0].ass_code_id)
                    org_ass_code.point -= 1
                    org_point = org_ass_code.point
                    org_id = org_ass_code.id
                    org_ass_code.save()

                org_vote = HaveVoted.objects.get(user_id=request.user.id,
                                                 ass_code__ass_id=ass_id)
                org_vote.ass_code_id = ass_code_id
                org_vote.save()

            else:
                HaveVoted.objects.create(user_id=request.user.id,
                                         ass_code_id=ass_code_id)

                # sql = """
                #     insert into assessment_havevote
                #     (user_id, ass_code_id, ass_id) value
                #     (%d, %d, %d)
                # """ % (request.user.id, ass_code_id, ass_id)
                #
                # execute_sql(sql)

            ass_code = AssessmentCode.objects.get(id=ass_code_id)
            ass_code.point += 1
            point = ass_code.point
            ass_code.save()

        sql = '''
            select SUM(point) 
            from assessment_assessmentcode 
            where ass_id = %d;
        ''' % ass_id

        sum_of_point = float(execute_sql(sql)[0][0])

        try:

            point = int(point / sum_of_point * 100)
            org_point = int(org_point / sum_of_point * 100)

        except ZeroDivisionError:

            point = 0
            org_point = 0

        response = JsonResponse({"point": point, "org_point": org_point, "org_code": org_id})

    elif post_type == "delete":

        have_delete = False
        comment_id = int(request.POST["comment_id"])
        choice_comment = Comment.objects.get(pk=comment_id)

        if choice_comment.user == request.user:
            choice_comment.delete()
            have_delete = True

        response = JsonResponse({"have_delete": have_delete})
    else:
        response = JsonResponse({})

    return response


@login_required
def assessment_add(request, pk):
    if not request.user.is_superuser:
        raise Http404("not exist")

    template = "assessment/seven.html"
    choice_assessment = Assessment.objects.get(pk=pk)

    if request.method == "GET":
        all_content = Content.objects.filter(assessment_id=pk)

        assessment_lists = [assessment_list(i, request.user) for i in Lesson.objects.all()]

        for i in assessment_lists:
            print(i.assessments)

        return render(request, template, {
            "all_content": all_content,
            "assessment_lists": assessment_lists,
            "pk": pk
        })

    # data = request.POST.get("data[0][]")
    datas = dict(request.POST)
    number = int(datas["number"][0])
    size = len(choice_assessment.content_set.all())

    count = number if number > size else size

    for i in range(count):
        if i < number:
            data = datas["data[%d][]" % i]

            data_type = data[1]
            value = data[2]
        else:
            temp = Content.objects.get(assessment=choice_assessment, number=i)
            temp.delete()

            continue

        temp = Content.objects.get_or_create(assessment=choice_assessment, number=i)[0]

        temp.reset_type()

        if data_type == "text":
            temp.isText = True
        elif data_type == "code":
            temp.isCode = True
        elif data_type == "title":
            temp.isTitle = True
        elif data_type == "subtitle":
            temp.isSubTitle = True
        elif data_type == "table":
            temp.isTable = True
        elif data_type == "image":
            temp.isImage = True
            if '/' in value:
                temp.content = value
            else:
                temp.content = "assessment_image/%d/%s" % (pk, value)
                print("assessment_image/%d/%s" % (pk, value))
            temp.save()
            continue

        temp.content = value

        temp.save()

    return JsonResponse({})
