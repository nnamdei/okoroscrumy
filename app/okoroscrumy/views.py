from django.shortcuts import render,redirect
from django.http import Http404,HttpResponse
from django.contrib import messages
from .models import ScrumyGoals,GoalStatus,ScrumyUser
from .forms import ChangeTaskStatusForm
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User, Group


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
    return render(request, 'okoroscrumy/goal.html', context)

class GoalIndexView(generic.ListView):
    template_name = 'okoroscrumy/goals.html'

    def get_queryset(self):
        return ScrumyGoals.objects.all()


class add_task(CreateView):
    model = ScrumyGoals
    fields = '__all__'
    success_url = '/app'

def ChangeTaskStatus(request, goal_id):
    message = ''
    if request.user.is_authenticated:
        current_user = request.user
        current_user_group = current_user.groups.all()
        if current_user_group :
            if request.method =="POST":
                form = ChangeTaskStatusForm(request.POST)
                if form.is_valid:
                    new_status = request.POST.get('status_id')
                    status_object = GoalStatus.objects.get(id=new_status)
                    try:
                        goal = ScrumyGoals.objects.get(id=goal_id)
                        goal_status = goal.status_id
                    except ScrumyGoals.DoesNotExist:
                        raise Http404('No goal assigned with the id ' + str(goal_id))

                    if str(current_user_group[0]) == 'OWNER':
                        goal.status_id = status_object

                    elif str(current_user_group[0]) == 'QUALITY ANALYST':
                        if str(goal_status) == 'V' and status_object.status == 'D':
                            goal.status_id = status_object
                        else:
                            print('Access denied to move this status')

                    elif str(current_user_group[0]) == 'DEVELOPER':
                        if str(goal_status) == 'WT' and status_object.status == 'DT':
                            goal.status_id = status_object
                        else :
                            print('Access denied to move this status')
                    else:
                        message += 'You do not have permission to change this goal status'
                        return HttpResponse('No permission defined for this group')
                    goal.save()
                    return redirect('app:index')

                else:
                    form = ChangeTaskStatusForm()
                context = {'form':form}
                return render(request, 'okoroscrumy/changestatus.html',context)

            else:
                print('user does not belong to any group')
                return HttpResponse('user does not belong to any group')
        else:
                return HttpResponse('Access denied, you have to sign in to continue')



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
