from rest_framework import generics
from .models import Flight
from .serializers import FlightSerializer
# Create your views here.
class CreateView(generics.ListCreateAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    def perform_create(self, serializer):
        serializer.save()


class DetailsView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Flight.objects.all()
    serializer_class = FlightSerializer