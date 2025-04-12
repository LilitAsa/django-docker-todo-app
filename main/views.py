from django.shortcuts import render, get_object_or_404, redirect
from .models import Todos

def index(request):
    todos = Todos.objects.all()
    
    return render(request, "main/home.html", {"todos":todos})