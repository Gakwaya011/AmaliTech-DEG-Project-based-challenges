from rest_framework import serializers
from .models import Monitor

class MonitorSerializer(serializers.ModelSerializer):
    # In the payload, they call it "id", but in our database, we called it "device_id"
    id = serializers.CharField(source='device_id')

    class Meta:
        model = Monitor
        fields = ['id', 'timeout', 'alert_email', 'status', 'last_ping']
        # The client shouldn't be able to manually set their status or ping time on creation
        read_only_fields = ['status', 'last_ping']