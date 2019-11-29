from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from table.models import Table


@login_required
def css_guide(request):
    return render(request, 'pages/css_guide.html', {})


def handler404(request, exception):
    return render(request, 'pages/handler404.html', {})


def handler500(request):
    return render(request, 'pages/handler500.html', {})


class TableView():

    def __init__(self, table):
        pass


def homepage(request):

    tables = Table.obs.all()


    context = {
            'tables': tables,
        }
    return render(request, 'pages/homepage.html', context)
