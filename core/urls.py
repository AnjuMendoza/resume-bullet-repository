from django.urls import path
from . import views

urlpatterns = [
    path('', views.bullet_list, name='bullet_list'),
    path('repository/', views.repository_view, name='repository'),
    path('repository/sections/add/', views.add_section, name='add_section'),
    path('repository/sections/reorder/', views.reorder_sections, name='reorder_sections'),
    path('repository/sections/<int:section_id>/', views.repository_view, name='repository_section'),
    path('repository/sections/<int:section_id>/update/', views.update_section, name='update_section'),
    path('repository/sections/<int:section_id>/delete/', views.delete_section, name='delete_section'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
]
