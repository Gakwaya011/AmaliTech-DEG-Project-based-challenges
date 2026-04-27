from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Monitor
from .serializers import MonitorSerializer


@api_view(['POST'])
def create_monitor(request):
    """
    Registers a new device monitor and initializes its timeout sequence.
    """
    serializer = MonitorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        
        # TODO: Dispatch Celery task to handle the countdown timer
        
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
    
    # TODO: Revoke existing Celery timeout task and spawn a new one

    return Response({"message": f"Heartbeat received for {device_id}"}, status=status.HTTP_200_OK)