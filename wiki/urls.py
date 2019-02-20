from django.urls import path, include
from . import views

app_name = 'wiki'

urlpatterns = [
    path('<int:lesson>/<int:chapter>', views.wiki, name="wiki"),
]
