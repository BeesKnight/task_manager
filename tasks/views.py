from django.contrib.auth.decorators import login_required
from django.db.models import Case, IntegerField, Value, When
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import TaskForm
from .models import Task


def index(request):
    return render(request, 'tasks/index.html')


@login_required
def task_list(request):
    priority_order = Case(
        When(priority=Task.HIGH, then=Value(0)),
        When(priority=Task.NORMAL, then=Value(1)),
        When(priority=Task.LOW, then=Value(2)),
        default=Value(3),
        output_field=IntegerField(),
    )
    due_order = Case(
        When(due_date__isnull=True, then=Value(1)),
        default=Value(0),
        output_field=IntegerField(),
    )
    tasks = (
        Task.objects.filter(owner=request.user)
        .annotate(priority_order=priority_order, due_order=due_order)
        .order_by('completed', 'priority_order', 'due_order', 'due_date', '-date_added')
    )
    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'now': timezone.now()})


@login_required
def new_task(request):
    if request.method != 'POST':
        form = TaskForm()
    else:
        form = TaskForm(data=request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            return redirect('tasks:task_list')

    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Новая задача'})


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)

    if request.method != 'POST':
        form = TaskForm(instance=task)
    else:
        form = TaskForm(instance=task, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:task_list')

    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Редактирование задачи'})


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)

    if request.method == 'POST':
        task.delete()
        return redirect('tasks:task_list')

    return render(request, 'tasks/confirm_delete.html', {'task': task})


@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, owner=request.user)

    if request.method == 'POST':
        task.completed = not task.completed
        task.save()

    return redirect('tasks:task_list')
