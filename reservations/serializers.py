from rest_framework import serializers

from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            "id",
            "event",
            "profile",
            "seats_reserved",
            "status",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = ["status", "created_at", "updated_at", "created_by", "updated_by"]

    def validate_seats_reserved(self, value):
        if value < 1:
            raise serializers.ValidationError("Must reserve at least 1 seat.")
        return value

    def validate(self, data):
        event = data.get('event')
        if event.status not in ('upcoming', 'ongoing'):
            raise serializers.ValidationError(
                f"Cannot reserve seats for a {event.status} event."
            )
        if data.get('seats_reserved', 0) > event.available_seats:
            raise serializers.ValidationError(
                f"Only {event.available_seats} seat(s) available."
            )
        return data

    def create(self, validated_data):
        event = validated_data['event']
        event.available_seats -= validated_data['seats_reserved']
        event.save()
        return Reservation.objects.create(**validated_data)
