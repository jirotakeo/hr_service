from django.shortcuts import render
import datetime


def home(request):
    date = datetime.datetime.now().date()
    name = 'jiro'
    context = {'name': name, 'date': date}
    return render(request, 'base.html', context)
