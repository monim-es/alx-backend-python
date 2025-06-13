from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
# select_related
# Message.objects.filter
@require_http_methods(["DELETE"])
@login_required
def delete_user(request):
    user = request.user
    username = user.username
    user.delete()
    return JsonResponse({"message": f"User '{username}' and related data deleted successfully."})


# sender=request.user  receiver
# Message.unread.unread_for_user.only
