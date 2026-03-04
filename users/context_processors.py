from chat.models import Message
from django.db.models import Q


def header_counters(request):
    if not request.user.is_authenticated:
        return {
            'unread_chat_count': 0,
            'unread_notifications_count': 0,
        }

    unread_chat_count = Message.objects.filter(
        Q(conversation__student=request.user) | Q(conversation__tutor=request.user),
        is_read=False,
    ).exclude(sender=request.user).count()

    unread_notifications_count = request.user.notifications.filter(is_read=False).count()

    return {
        'unread_chat_count': unread_chat_count,
        'unread_notifications_count': unread_notifications_count,
    }
