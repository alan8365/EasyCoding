from django.urls import path, include
from . import views

app_name = 'assessment'

urlpatterns = [
    path('', views.assessment, name="assessment_for_precess"),
    path('<int:pk>', views.assessment, name="assessment"),
    path('vote/<int:pk>', views.vote, name="vote"),
    path('vote/<int:pk>/<str:sort_by>', views.vote, name="vote"),
    path('vote/<int:pk>/<str:sort_by>/<int:page>', views.vote, name="vote"),
    path('assessment_add/<int:pk>', views.assessment_add, name="assessment_add"),
]
