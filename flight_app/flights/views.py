from rest_framework import generics
from .models import Tickets, AvailableFlights
from .serializers import  ListFlightSerializer, FlightSerializer
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from flight_app.settings import SECRET_KEY
from rest_framework.authtoken.models import Token
from django.core import serializers
from flight_app.tasks import send_notification_email_task

class ListFlightView(APIView):
    serializer_class = ListFlightSerializer
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        if request.META['HTTP_AUTHORIZATION']:
            token = request.META['HTTP_AUTHORIZATION']
            user_id = Token.objects.values_list('user_id', flat=True).get(key=token)
            origin = request.data['origin']
            destination = request.data['destination']
            date = request.data['date']
            flight_exists = AvailableFlights.objects.filter(origin=origin,destination=destination,date__contains = date, available_seats__gt=0)
            serializer = ListFlightSerializer(flight_exists, many=True)
            return Response(serializer.data)
        return Response('No token provided')
class CreateView(APIView):
    serializer_class = FlightSerializer
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        if request.META['HTTP_AUTHORIZATION']:
            token = request.META['HTTP_AUTHORIZATION']
            user_id = Token.objects.values_list('user_id', flat=True).get(key=token)
            origin = request.data['origin']
            destination = request.data['destination']
            date = request.data['date']
            seat = request.data['seat']
            airline = request.data['airline']
            flight_exists = AvailableFlights.objects.filter(origin=origin,destination=destination,date__contains = date, available_seats__gt=0, airline=airline).first()
            if flight_exists:
                if seat in flight_exists.seats['seats']:
                    serializer = FlightSerializer(data={'origin':flight_exists.origin,
                                                        'destination':flight_exists.destination,
                                                        'date':flight_exists.date,
                                                        'airline':flight_exists.airline,
                                                        'plane_number':flight_exists.plane_number,
                                                        'seat_number':seat,
                                                        'user':user_id})
                    if serializer.is_valid():
                        serializer.save()
                        flight_exists.seats['seats'].pop(flight_exists.seats['seats'].index(seat))
                        flight_exists.available_seats = flight_exists.available_seats - 1
                        flight_exists.save()
                        send_notification_email_task.apply_async(args=[request.data['name'],request.data['email'],'Welcome'], eta=date - timedelta(seconds=86400))
                        return Response(serializer.data)
                else:
                    return Response('Seat doesnt exist')
            return Response('Flight doesnt exist')
        return Response('No token provided')



class DetailsView(APIView):

    permission_classes = (permissions.AllowAny,)
    serializer_class = FlightSerializer

    def post(self, request, format=None):
        if request.META['HTTP_AUTHORIZATION']:
            token = request.META['HTTP_AUTHORIZATION']
            user_id = Token.objects.values_list('user_id', flat=True).get(key=token)
            if user_id:
                flights = Tickets.objects.filter(user_id=user_id).all()
                serializer = FlightSerializer(flights, many=True)
                return Response(serializer.data)
            else:
                Response('Invalid Token!')
        return Response('No token provided')