from apps.logs.models import LogEntry

def log_entry(user, level, message):
    try:
        print("User: " + user.username + " - Level: " + level + " - Message: " + message)
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