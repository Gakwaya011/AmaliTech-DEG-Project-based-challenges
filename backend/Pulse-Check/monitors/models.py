from django.db import models
from django.utils import timezone

class Monitor(models.Model):
    STATUS_CHOICES = [
        ('up', 'Up'),
        ('down', 'Down'),
        ('paused', 'Paused'), # We are adding this now for the Bonus User Story
    ]

    # We use device_id as the primary key since their payload uses {"id": "device-123"}
    device_id = models.CharField(max_length=255, primary_key=True)
    timeout = models.IntegerField(help_text="Timeout in seconds before alert fires")
    alert_email = models.EmailField()
    
    # State tracking
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='up')
    last_ping = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.device_id} - {self.status}"