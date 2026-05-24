from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    reservations_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "title",
            "venue",
            "date",
            "status",
            "total_seats",
            "available_seats",
            "reservations_count"
        ]
        read_only_fields = ["created_by", "updated_by", "created_at", "updated_at"]

    def get_reservations_count(self, obj):
        return obj.event_reservations.filter(status='confirmed').count()

    def validate(self, data):
        available_seats = data.get('available_seats')
        total_seats = data.get('total_seats')

        if available_seats > total_seats:
            raise serializers.ValidationError("available_seats cannot exceed total_seats.")

        return data
