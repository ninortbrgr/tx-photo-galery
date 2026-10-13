from django.http import HttpResponse
from django.shortcuts import render
import random

def index(request):
    name = "Django"
    random_number = random.randint(1, 100)
    return render(request, 'index.html', {'name': name, 'random_number': random_number})