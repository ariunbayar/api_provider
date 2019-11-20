from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def css_guide(request):
    return render(request, 'pages/css_guide.html', {})

