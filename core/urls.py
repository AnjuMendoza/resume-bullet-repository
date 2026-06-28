from django.urls import path
from . import views

urlpatterns = [
    path('', views.bullet_list, name='bullet_list'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
]
