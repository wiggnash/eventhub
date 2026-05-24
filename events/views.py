from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# models imports
from .models import Event

# serializer imports
from .serializers import EventSerializer

# Create your views here.
class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_class = [IsAuthenticated]
    queryset = Event.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def get_queryset(self):
        queryset = Event.objects.all()
        status = self.request.query_params.get('status')
        venue = self.request.query_params.get('venue')

        if status:
            queryset = queryset.filter(status=status)

        if venue:
            queryset = queryset.filter(venue__icontains=venue)

        return queryset

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user
        )

    def perform_update(self, serializer):
        serializer.save(
            updated_by=self.request.user
        )
