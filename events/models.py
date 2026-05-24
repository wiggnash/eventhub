from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Event(models.Model):
    STATUS_CHOICES=[
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    title=models.CharField(max_length=200)
    venue=models.CharField(max_length=200)
    date=models.DateField()
    total_seats=models.PositiveIntegerField()
    available_seats=models.PositiveIntegerField()
    status=models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')

    # audit fields
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    created_by=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_events')
    updated_by=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_events')

    def __str__(self):
        return f"{self.title} at {self.venue}"

    class Meta:
        ordering = ["date"]
