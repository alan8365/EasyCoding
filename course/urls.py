from django.urls import path, include
from . import views

app_name = 'course'

urlpatterns = [
    path('', views.course, name="course_for_process"),
    path('<int:lesson_number>/<int:chapter>', views.course, name="course"),
    path('course_add/<int:lesson_number>/<int:chapter>', views.course_add, name="course_add")
]
