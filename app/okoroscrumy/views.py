from .forms import AddUserForm
from django.shortcuts import render,redirect
from .models import ScrumyGoals,GoalStatus,ScrumyUser


def index(request):
    goals = ScrumyGoals.objects.all()
    context = {'goals':goals}
    return render(request, okoroscrumy/index.html, context)

def get_users(request):
    users = ScrumyUser.objects.all()
    context = {'users':users}
    return render(request, 'okoroscrumy/users.html', context)

def add_user(request):
    if request.method == "POST":
        form = AddUserForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('users')
        else:
            form = AddUserForm()
            context = {'form':form}
            return render(request, 'okoroscrumy/adduser.html', context)

def dailytask_goals(request):
    status_dt= GoalStatus.objects.get(status='DT')
    goals = status_dt.scrumygoals_set.all()
    context = {'goals':goals}
    return render(request, okoroscrumy/dailytask.html, context)

def move_goal(request, task_id):
    goals = ScrumyGoals.objects.filter(task_id=task_id)
    context = { 'goals':goals, 'task_id':task_id}
    return render(request, 'okoroscrumy/goals.html', context)
