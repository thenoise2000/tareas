
from .models import Sender


def allnotifications(request):
    notifications = None
    if request.user.is_authenticated:
        notifications = Sender.objects.filter(user=request.user).order_by('-created_date')[0:3]
    return {'notifications': notifications}