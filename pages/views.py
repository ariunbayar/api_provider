from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def css_guide(request):
    return render(request, 'pages/css_guide.html', {})


def handler404(request, exception):
    return render(request, 'pages/handler404.html', {})


def handler500(request):
    return render(request, 'pages/handler500.html', {})
