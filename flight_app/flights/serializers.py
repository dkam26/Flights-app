from rest_framework import serializers
from .models import Tickets, AvailableFlights

# class FlightSerializer(serializers.ModelSerializer):


#     class Meta:
#         model = Flight
#         fields = ('id' , 'user', 'origin', 'destination', 'flight_date')



class ListFlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableFlights
        fields = ('airline', 'origin', 'destination',
    'available_seats',
    'date',
    'plane_number',
    'seats' )


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model =Tickets
        fields = ('airline',
    'origin',
    'destination',
    'date',
    'plane_number',
    'seat_number',
    'user',)
