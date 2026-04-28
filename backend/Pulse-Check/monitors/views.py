from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Monitor
from .serializers import MonitorSerializer
from .tasks import check_device_timeout  

@api_view(['POST'])
def create_monitor(request):
    """
    Registers a new device monitor and initializes its timeout sequence.
    """
    serializer = MonitorSerializer(data=request.data)
    if serializer.is_valid():
        monitor = serializer.save()
        
        # Dispatch Celery task to check status after the exact timeout period
        check_device_timeout.apply_async(args=[monitor.device_id], countdown=monitor.timeout)
        
        return Response(
            {"message": "Monitor created successfully.", "data": serializer.data}, 
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def heartbeat(request, device_id):
    """
    Receives a ping from a remote device, resetting its timeout sequence.
    """
    # Fetch the device or return a 404 per API requirements
    monitor = get_object_or_404(Monitor, device_id=device_id)
    
    # Reset the heartbeat timestamp and mark status as active
    monitor.last_ping = timezone.now()
    monitor.status = 'up' 
    monitor.save()
    
    # Spawn a new timeout check. 
    check_device_timeout.apply_async(args=[monitor.device_id], countdown=monitor.timeout)

    return Response({"message": f"Heartbeat received for {device_id}"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def pause_monitor(request, device_id):
    """
    Pauses the monitor to prevent false alarms during maintenance.
    """
    monitor = get_object_or_404(Monitor, device_id=device_id)
    
    # Change state to paused so the Celery task ignores it
    monitor.status = 'paused'
    monitor.save()
    
    return Response({"message": f"Monitoring paused for {device_id}"}, status=status.HTTP_200_OK)