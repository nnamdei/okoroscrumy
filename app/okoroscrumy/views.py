from django.shortcuts import render,redirect
from django.http import Http404
from django.contrib import messages
from .models import ScrumyGoals,GoalStatus,ScrumyUser
from .forms import ChangeTaskStatusForm
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView

def index(request):
    users = ScrumyUser.objects.all()
    context = {'users':users}
    return render(request, 'okoroscrumy/index.html', context)

def get_users(request):
    users = ScrumyUser.objects.all()
    context = {'users':users}
    return render(request, 'okoroscrumy/users.html', context)

class add_user(CreateView):

    model = ScrumyUser
    fields = '__all__'
    success_url = '/app'

def dailytask_goals(request):
    status_dt= GoalStatus.objects.get(status='DT')
    goals = status_dt.scrumygoals_set.all()
    context = {'goals':goals}
    return render(request, 'okoroscrumy/dailytask.html', context)

def move_goal(request, task_id):
    try:
        goals = ScrumyGoals.objects.get(task_id=task_id)
    except ScrumyGoals.DoesNotExist:
        raise Http404('No goal with this task_id' + str(task_id))
    context = {'goals':goals, 'task_id':task_id}
    return render(request, 'okoroscrumy/goals.html', context)

class add_task(CreateView):
    model = ScrumyGoals
    fields = '__all__'
    success_url = '/app'

def ChangeTaskStatus(request, goal_id):
    if request.method == "POST":
        form = ChangeTaskStatusForm(request.POST)
        if form.is_valid:
            NewStatus = request.POST.get('status_id')
            status = GoalStatus.objects.get(id=NewStatus)
            try:
                goal = ScrumyGoals.objects.get(id=goal_id)
            except ScrumyGoals.DoesNotExist:
                raise Http404('No goal with this id' + str(goal_id))
            goal.status_id = status
            goal.save()
            return redirect('okoroscrumy:index')
    else:
        form = ChangeTaskStatusForm()
        context = {'form':form}
        return render(request, 'okoroscrumy/changestatus.html', context)
