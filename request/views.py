from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Request


@login_required
def list(request):

    requests = Request.objects.all()[:40]

    context = {
            'requests': requests,
        }

    return render(request, 'request/list.html', context)
