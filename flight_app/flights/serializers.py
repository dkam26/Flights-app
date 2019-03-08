from rest_framework import serializers
from .models import Flight

class FlightSerializer(serializers.ModelSerializer):


    class Meta:
        model = Flight
        fields = ('id' , 'user', 'origin', 'destination', 'flight_date')