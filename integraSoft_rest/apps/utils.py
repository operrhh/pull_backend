from apps.logs.models import LogEntry

def log_entry(user, level: str, module: str,message: str):
    try:
        LogEntry.objects.create(
            user=user,
            level=level,
            module=module,
            message=message
        )
    except Exception as e:
        LogEntry.objects.create(
            user=user,
            level='ERROR',
            message=f'Error en log_entry: {str(e)}'
        )