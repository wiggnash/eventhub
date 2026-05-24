from django.contrib.auth.models import User
from django.db import models

#models imports
from events.models import Event
from profiles.models import Profile

# Create your models here.
class Reservation(models.Model):
    STATUS_CHOICES=[
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    # relations
    event=models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='event_reservations'
    )
    profile=models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="profile_reservations"
    )

    # columns
    seats_reserved=models.PositiveIntegerField()
    status=models.CharField(max_length=50, choices=STATUS_CHOICES, default='confirmed')

    # audit fields
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    created_by=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_reservations')
    updated_by=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_reservations')

    def __str__(self):
        return f"{self.profile.email} {self.event.title} {self.seats_reserved}"

    class Meta:
        ordering=["-created_at"]
