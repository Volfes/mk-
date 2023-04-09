from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register_user, name='register_user'),
    path('login', views.login_user, name='login_user'),
    path('', views.home_page, name='home_page'),
    path('logout', views.logout_user, name='logout_user'),
    path('update_password/', views.change_password, name='change_password'),
    path('profile', views.profile, name='profile'),
    path('update_email/', views.change_email, name='change_email'),
]   
