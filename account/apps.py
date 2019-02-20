from django.apps import AppConfig

from .achievement_condition import *
from .models import Achievement_get


class AccountConfig(AppConfig):
    name = 'account'


course_achievement_condition_list = {"start_lesson_%d" % i: get_start_lesson(i) for i in range(1, 9)}

assessment_achievement_condition_list = {
    "first_complete_assessment": start_programme,
    "code_bronze": code_bronze,
    "code_silver": code_silver,
    "code_gold": code_gold
}


def course_achievement_check(user):
    for name, condition in course_achievement_condition_list.items():

        if condition(user):
            Achievement_get.objects.create(achievement_id=name, user=user)


def assessment_achievement_check(user):
    for name, condition in assessment_achievement_condition_list.items():

        if condition(user):
            Achievement_get.objects.create(achievement_id=name, user=user)
