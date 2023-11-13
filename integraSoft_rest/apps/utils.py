from apps.logs.models import LogEntry
from django.contrib.auth.decorators import login_required

@login_required
def log_entry(user, level, message):
    try:
        LogEntry.objects.create(
            user=user,
            level=level,
            message=message
        )
    except Exception as e:
        LogEntry.objects.create(
            user=user,
            level='ERROR',
            message=f'Error en log_entry: {str(e)}'
        )