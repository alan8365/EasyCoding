from django.urls import path, include
from . import views

app_name = 'tutorial'

urlpatterns = [
    path('', views.home, name="home"),
    path('course/<int:lesson_number>/<int:chapter>', views.course, name="course"),
    path('assessment/<int:pk>', views.assessment, name="assessment"),
    path('vote/<int:pk>/<str:sort_by>/<int:page>', views.vote, name="vote"),
]
