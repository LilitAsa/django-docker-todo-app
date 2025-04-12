from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib.auth import get_user_model


def register_view(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users:profile')
        else:
            form = CustomUserCreationForm()
            print(form.errors) 
    return render(request, 'users/register.html', {'form': form, 'errors': form.errors})
 
 
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm()
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('users:profile')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('users:login')


@login_required
def profile_view(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        # If task form is being submitted
        if "title" in request.POST:
            task_form = TaskForm(request.POST)
            profile_form = ProfileForm(instance=user_profile)

            if task_form.is_valid():
                task = task_form.save(commit=False)
                task.user_profile = user_profile  # Associate task with the user's profile
                task.check_flags()  # Update flags after saving the task
                task.save()
                return redirect("users:profile")  # Redirect to profile after task creation
        # If profile form is being submitted
        else:
            task_form = TaskForm()
            profile_form = ProfileForm(request.POST, instance=user_profile)

            if profile_form.is_valid():
                profile_form.save()  # Save the profile form with updated data
                return redirect("users:profile")  # Redirect to profile after saving
    else:
        # GET request - display empty forms with user data
        task_form = TaskForm()
        profile_form = ProfileForm(instance=user_profile)

    return render(request, "users/profile.html", {
        "user_profile": user_profile,
        "profile_form": profile_form,
        "task_form": task_form,
    })

@login_required
def edit_profile_view(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=user_profile)

    return render(request, 'users/edit_profile.html', {'form': form})

def delete_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        user_profile.delete()
        logout(request)
        return redirect('users:login')

    return render(request, 'users/confirm_delete_profile.html', {'user_profile': user_profile})


@login_required
def edit_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, user_profile__user=request.user)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = TaskForm(instance=task)

    return render(request, 'users/edit_task.html', {'form': form})

@login_required
def delete_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, user_profile__user=request.user)
    
    if request.method == "POST":
        task.delete()
        return redirect('users:profile')

    # Optional: confirm delete page
    return render(request, 'users/confirm_delete.html', {'task': task})


@login_required
def delete_profile_view(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        user_profile.delete()
        logout(request)
        return redirect('users:login')

    return render(request, 'users/confirm_delete_profile.html', {'user_profile': user_profile})

@login_required
def task_list_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    tasks = Task.objects.filter(user_profile=user_profile)
    return render(request, 'users/task_list.html', {'tasks': tasks})

@login_required
def task_detail_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, user_profile__user=request.user)
    return render(request, 'users/task_detail.html', {'task': task})

@login_required
def complete_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, user_profile__user=request.user)
    task.is_completed = True
    task.save()
    return redirect('users:task_list_view')

@login_required
def uncomplete_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, user_profile__user=request.user)
    task.is_completed = False
    task.save()
    return redirect('users:task_list_view')

@login_required
def change_task_status_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, user_profile__user=request.user)
    task.is_completed = not task.is_completed
    task.save()
    return redirect('users:task_list_view')

@login_required
def task_list_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    tasks = Task.objects.filter(user_profile=user_profile)
    return render(request, 'users/task_list.html', {'tasks': tasks})



