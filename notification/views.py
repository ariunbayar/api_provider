from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from notification.models import Notification


@login_required
@csrf_exempt
def mark_as_read(request):
    pk = request.POST.get('pk')
    Notification.objects.filter(pk=pk, user=request.user, is_read=False).update(is_read=True)
    context = {
            'success': True,
        }
    return JsonResponse(context)
