from django.apps import AppConfig
from django.db import connection

# from assessment.code.answer.lib import function_name
from .models import AssessmentCode
from account.models import User
from assessment.models import Comment
import subprocess


class CourseConfig(AppConfig):
    name = 'assessment'


def execute_sql(sql):
    with connection.cursor() as c:
        c.execute(sql)
        value = c.fetchall()

    return value


def update_assess_code(user_id, ass_id, code):
    sql = """
        select id
        from assessment_assessmentcode
        where user_id = %d and ass_id = %d
    """ % (user_id, ass_id)

    repeat_test = execute_sql(sql)

    if repeat_test:
        ac = AssessmentCode.objects.get(pk=repeat_test[0][0])

        ac.delete()

    AssessmentCode.objects.create(
        user_id=user_id,
        ass_id=ass_id,
        point=0,
        code=code
    )


def execute_user_code(user_file, answer_function, input_value):
    answer = str(answer_function(input_value))

    user_process = subprocess.Popen(
        ['python', user_file],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        universal_newlines=True
    )

    output = '輸入:%d\n' % input_value
    is_answer_right = False

    try:
        user_outs, user_errs = user_process.communicate(timeout=10, input=str(input_value))

        if user_errs:
            output += "輸出:%s\n" % user_errs
            output = "<red>錯誤</red>\n" + output
        else:
            output += "輸出:%s\n" % user_outs

            if answer == user_outs:
                output = "<green>正確</green>\n" + output
                is_answer_right = True
            else:
                output = "<red>錯誤</red>,答案應為:%s\n" % answer + output

    except subprocess.TimeoutExpired:
        user_process.kill()
        output = 'timeout'

    return output, is_answer_right


def check_all_answer_right(answers):
    for answer in answers:
        if not answer:
            return False

    return True


class AssessmentCodeContent:

    def __init__(self, id, user, point_percent, code, read_user_id, datetime):
        self.id = id
        self.user = user

        self.point_percent = point_percent
        self.datetime = datetime

        self.code = code
        self.main_comments = []

        sql = '''
            select `id`, `like`, `dislike`, `date`, `content`, `user_id`
            from assessment_comment where reply_id is null and ass_code_id = %s
            order by date DESC
        ''' % id

        temp = execute_sql(sql)

        for i in temp:
            self.main_comments.append(
                CommentContent(
                    stuff=i,
                    is_main=True,
                    ass_code_id=id,
                    read_user_id=read_user_id
                )
            )

    def __repr__(self):
        return "%s" % str(self.user)


# id, like, dislike, datetime, content, user_id

class CommentContent:

    def __init__(self, stuff, is_main=False, ass_code_id=None,
                 read_user_id=None):
        if isinstance(stuff, tuple):
            self.id = stuff[0]
            self.like = stuff[1]
            self.dislike = stuff[2]
            self.datetime = stuff[3]
            self.content = stuff[4]
            self.user = User.objects.get(pk=stuff[5])

        elif isinstance(stuff, Comment):
            self.id = stuff.id
            self.like = stuff.like
            self.dislike = stuff.dislike
            self.datetime = stuff.date
            self.content = stuff.content
            self.user = stuff.user

        sql = '''
            select is_like 
            from assessment_havelike
            where user_id = %d and comment_id = %d
        ''' % (read_user_id, self.id)

        liked = execute_sql(sql)

        if not liked:
            self.like_status = None
        elif liked[0][0]:
            self.like_status = True
        else:
            self.like_status = False

        if is_main:
            self.replies = []

            sql = '''
                select `id`, `like`, `dislike`, `date`, `content`, `user_id`
                from assessment_comment where reply_id = %s and ass_code_id = %s
                order by date DESC
            ''' % (self.id, ass_code_id)

            temp = execute_sql(sql)

            for j in temp:
                self.replies.append(
                    CommentContent(
                        stuff=j,
                        read_user_id=read_user_id,
                    )
                )

    def __repr__(self):
        return "%s:%s" % (str(self.user), str(self.content))


def get_vote_content_by_id(id, read_user_id):
    sql = """
        select ac.id, user.id, point, code, datetime 
        from assessment_assessmentcode as ac, account_user as user
        where ass_id = %d and ac.user_id = user.id
    """ % id

    all_user_info = execute_sql(sql)
    contents = []

    sql = '''
        select SUM(point) 
        from assessment_assessmentcode 
        where ass_id = %d;
    ''' % id

    sum_of_point = float(execute_sql(sql)[0][0])

    for user_info in all_user_info:
        try:
            point_percent = int((float(user_info[2]) / sum_of_point) * 100)
        except ZeroDivisionError:
            point_percent = 0

        contents.append(
            AssessmentCodeContent(
                user_info[0],
                User.objects.get(pk=user_info[1]),
                point_percent,
                user_info[3],
                read_user_id,
                user_info[4],
            )
        )

    return contents


def list_split(li, x):
    ans = []

    start = 0
    stop = x

    while stop < len(li):
        ans.append(
            li[start:stop]
        )

        start += x
        stop += x

    ans.append(
        li[start:]
    )

    return ans


