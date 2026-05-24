from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Reservation
from .serializers import ReservationSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def get_queryset(self):
        queryset = Reservation.objects.all()
        event_id = self.request.query_params.get('event_id')
        if event_id:
            queryset = queryset.filter(event_id=event_id)
        return queryset

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        reservation = self.get_object()
        if reservation.status == 'cancelled':
            return Response({'error': 'Already cancelled.'}, status=400)

        reservation.event.available_seats += reservation.seats_reserved
        reservation.event.save()

        reservation.status = 'cancelled'
        reservation.save()

        return Response(self.get_serializer(reservation).data)
