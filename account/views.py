from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as user_login
from django.contrib.auth import logout as user_logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

from .forms import UserForm
from .models import User, Achievement, Achievement_get
from .apps import course_achievement_check, assessment_achievement_check

from assessment.models import Assessment
from assessment.apps import execute_sql

from EasyCoding.settings import BASE_DIR

from time import time
import os


def register(request):
    template = 'account/signup.html'
    if request.method == 'GET':
        return render(request, template)

    if 'type' in request.POST:
        if request.POST.get('type') == 'check_email':

            email = request.POST.get('email')

            repeat = True
            sql = """
                select id 
                from account_user
                where email = "%s"
            """ % email

            repeat_email = execute_sql(sql)

            if not repeat_email:
                repeat = False

            response = JsonResponse({"repeat": repeat})

        elif request.POST.get('type') == 'check_username':

            username = request.POST.get('username')

            repeat = True

            sql = """
                select id 
                from account_user
                where username = "%s"
            """ % username

            repeat_username = execute_sql(sql)

            if not repeat_username:
                repeat = False

            response = JsonResponse({"repeat": repeat})

        return response

    form = UserForm(request.POST)
    user = form.save()
    print(user)

    return login(request)


def forget_passwd(request):
    template = 'account/forgetpasswd'


def index(request):
    template = 'index.html'
    if request.method == 'GET':
        return render(request, template)


def login(request):
    template = 'account/login.html'
    if request.method == 'GET':
        return render(request, template)

    # GET
    next_page = request.GET.get('next')
    print(next_page)

    # POST
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username=username, password=password)

    if not user:
        return render(request, template, {'error': '登入失敗'})
    # login success
    user_login(request, user)

    if next_page:
        return redirect(next_page)
    else:
        return redirect('/')


@login_required
def logout(request):
    user_logout(request)
    messages.success(request, 'ㄅㄅ')
    return redirect('home')


@login_required
def profile(request):
    template = "account/profile.html"

    user = request.user

    result = profile_base(request, template, user)

    return result


def profile_for_other(request, username):
    template = "account/profile_for_other.html"

    user = User.objects.get(username=username)

    result = profile_base(request, template, user)

    return result


def profile_base(request, template, user):
    course_achievement_check(user)
    assessment_achievement_check(user)

    sql = """
        select sum(point)
        from assessment_assessmentcode as ac
        where ac.user_id = %d
    """ % user.id

    vote_sum = execute_sql(sql)[0][0]

    if vote_sum:
        user.vote_number = int(vote_sum)
    else:
        user.vote_number = 0

    user.save()

    assessment_level_completed = []

    for i in range(1, 6):
        sql = """
            SELECT COUNT(ac.id)
            FROM assessment_assessmentcode as ac, assessment_assessment as a 
            WHERE ac.user_id = %d and a.level = %d and ac.ass_id = a.id
        """ % (user.id, i)

        temp = execute_sql(sql)[0][0]

        assessment_level_completed.append(temp)

    temp = len(Assessment.objects.all()) - sum(assessment_level_completed) - 1
    assessment_level_completed.append(temp)

    all_vote_of_user = list(user.assessmentcode_set.all().exclude(ass__course__lesson__number=0))
    all_vote_of_user.sort()

    all_achievement_get = Achievement_get.objects.filter(user_id=user.id)
    all_achievement_get = [i.achievement for i in all_achievement_get]

    if len(all_achievement_get) > 2:
        all_achievement_get = list(all_achievement_get)
        all_achievement_get.sort(reverse=True)
        all_achievement_get = all_achievement_get[:2]

    if request.method == 'POST':
        update_img = request.FILES.get("update_img")

        fs = FileSystemStorage(
            location=os.path.join(BASE_DIR, "static/media/user_images")
        )

        fs.delete(user.username + ".png")
        filename = fs.save(user.username + ".png", update_img)
        update_url = fs.url(filename)

        user.image_url = "media/user_images/%s.png" % user.username
        user.save()

    return render(request, template, {
        "user": user,
        "assessment_level_completed": assessment_level_completed,
        "all_vote_of_user": all_vote_of_user,
        "all_achievement_get": all_achievement_get,
        "time": int(time())
    })


@login_required
def achievement(request):
    template = "account/achievement.html"

    user = request.user

    return achievement_base(request, template, user)


def achievement_for_other(request, username):
    template = "account/achievement.html"
    user = User.objects.get(username=username)

    return achievement_base(request, template, user)


def achievement_base(request, template, user):
    unlock_achievement = [i.achievement for i in user.achievement_get_set.all()]

    all_achievement = []
    temp = list(Achievement.objects.all())
    temp.sort()

    for little_achievement in temp:

        if little_achievement in unlock_achievement:
            little_achievement.is_unlock = True
            all_achievement.insert(0, little_achievement)
        else:
            little_achievement.is_unlock = False
            all_achievement.append(little_achievement)

    return render(request, template, {
        "user": user,
        "all_achievement": all_achievement
    })


def contact(request):
    template = "account/contact.html"

    return render(request, template)
