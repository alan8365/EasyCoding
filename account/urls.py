from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/<username>', views.profile_for_other, name='profile_for_other'),
    path('achievement/', views.achievement, name='achievement'),
    path('achievement/<username>', views.achievement_for_other, name='achievement_for_other'),
    path('contact/', views.contact, name='contact')
]
