from course.models import Course
from .models import Achievement
from assessment.apps import execute_sql


def never_get_achievement_required(achievement_name):
    def level_two_decorator(func):
        def result(user):
            achievement = Achievement.objects.get(name=achievement_name)

            if is_user_already_get_achievement(user, achievement):
                return False

            return func(user)

        return result

    return level_two_decorator


def get_start_lesson(number):
    @never_get_achievement_required("start_lesson_%d" % number)
    def result(user):
        base = Course.objects.get(lesson__number=number, chapter=1)

        return user.course_progress >= base

    return result


@never_get_achievement_required("first_complete_assessment")
def start_programme(user):
    return bool(user.assessmentcode_set.all())


@never_get_achievement_required("code_bronze")
def code_bronze(user):
    return user.vote_number > 10


@never_get_achievement_required("code_silver")
def code_silver(user):
    return user.vote_number > 25


@never_get_achievement_required("code_gold")
def code_gold(user):
    return user.vote_number > 50


def is_user_already_get_achievement(user, achievement):
    sql = """
        select a.achievement_id
        from account_user as u,
             account_achievement_get as a
        where a.user_id = u.id and u.id = %d
    """ % user.id

    result = execute_sql(sql)

    aid = achievement.name

    for i in result:
        if aid == i[0]:
            return True

    return False
