from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def add(request):
    return render(request, 'schema/add.html', {})


@login_required
def save(request):
    pass
