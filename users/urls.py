from django.urls import path
from .views import *

app_name = "users"

urlpatterns = [
  path("login/", login_view, name ='login'),
  path('register/', register_view, name='register'),
  path('profile/', profile_view, name='profile'),
  path('profile/edit/', edit_profile_view, name='edit_profile'),
  path('profile/delete/', delete_profile, name='delete_profile'),
  path("logout/", logout_view, name ='logout'),
  
  path('task/<int:task_id>/edit/', edit_task_view, name='edit_task'),
  path('task/<int:task_id>/delete/', delete_task_view, name='delete_task'),
  path('task/<int:task_id>/complete/', complete_task_view, name='complete_task'),
  path('task/<int:task_id>/incomplete/', uncomplete_task_view, name='uncomplete_task'),
  path('task/<int:task_id>/change-status/', change_task_status_view, name='change_task_status'),
  path('task/<int:task_id>/', task_detail_view, name='task_detail'),
  path('task/task-list/', task_list_view, name='task_list_view'),
]