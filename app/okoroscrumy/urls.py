from django.urls import path
from . import views

app_name = 'okoroscrumy'
urlpatterns = [
    path('', views.index, name ='index'),
    path('dailytask/', views.dailytask_goals, name='dailytask'),
    path('<int:task_id/>', views.move_goal, name='move_goal'),
    path('users/',views.get_users,name='users'),
    path('adduser/',views.add_user.as_view(),name='add_user'),
    path('addtask/', views.add_task.as_view(), name='add_task'),
    path('<int:goal_id>/changestatus/', views.ChangeTaskStatus, name='change_status'),
    path('goals/', views.GoalIndexView.as_view(), name='goals'),
]
