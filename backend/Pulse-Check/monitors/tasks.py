from celery import shared_task
from django.utils import timezone
from .models import Monitor
import json

@shared_task
def check_device_timeout(device_id):
    """
    Evaluates if a device missed its heartbeat window.
    If the time since last_ping exceeds the timeout, triggers an alert.
    """
    try:
        monitor = Monitor.objects.get(device_id=device_id)
    except Monitor.DoesNotExist:
        return

    # Skip alert if system is paused (Bonus Feature preparation)
    if monitor.status == 'paused':
        return

    # Calculate elapsed time in seconds
    time_since_ping = (timezone.now() - monitor.last_ping).total_seconds()

    # If the elapsed time is greater than or equal to the timeout limit, fire the alert
    if time_since_ping >= monitor.timeout:
        monitor.status = 'down'
        monitor.save()
        
        # Format the alert exactly as requested in Acceptance Criteria 3
        alert_payload = {
            "ALERT": f"Device {device_id} is down!",
            "time": timezone.now().isoformat()
        }
        print(json.dumps(alert_payload))