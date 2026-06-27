from django.urls import path
from . import views

urlpatterns = [
    path('', views.bullet_list, name='bullet_list'),
    path('logout/', views.logout_view, name='logout'),
]
