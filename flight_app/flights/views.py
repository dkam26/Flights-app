from rest_framework import generics
from flight_app.user.models import User
from flight_app.flights.models import Tickets, AvailableFlights
from flight_app.flights.serializers import  ListFlightSerializer, FlightSerializer
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from flight_app.flight_app.settings import SECRET_KEY
from rest_framework.authtoken.models import Token
from django.core import serializers
from flight_app.flight_app.tasks import send_notification_email_task
from datetime import datetime, timedelta

class ListFlightView(APIView):
    serializer_class = ListFlightSerializer
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        if 'HTTP_AUTHORIZATION' in list(request.META.keys()):
            if request.META['HTTP_AUTHORIZATION']:
                token = request.META['HTTP_AUTHORIZATION']
                user_id = Token.objects.values_list('user_id', flat=True).get(key=token)
                if user_id:
                    json_keys = list(request.data.keys())
                    if json_keys == ['origin', 'destination']:
                        origin = request.data['origin']
                        destination = request.data['destination']
                        if origin and destination:
                            flight_exists = AvailableFlights.objects.filter(origin=origin,destination=destination, available_seats__gt=0)
                            serializer = ListFlightSerializer(flight_exists, many=True)
                            return Response(serializer.data)
                        return Response({'Message':'Missing input'})
                    return Response({'Message':'Invalid Json keys'})
                return Response({'Message':'Invalid token'})
            return Response({'Message':'No token provided'})
        return Response({'Message':'Missing token key'})
class CreateView(APIView):
    serializer_class = FlightSerializer
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        if 'HTTP_AUTHORIZATION' in list(request.META.keys()):
            if request.META['HTTP_AUTHORIZATION']:
                token = request.META['HTTP_AUTHORIZATION']
                user_id = Token.objects.values_list('user_id', flat=True).get(key=token)

                if list(request.data.keys()) == ['origin', 'destination','date','seat','airline']:
                    origin = request.data['origin']
                    destination = request.data['destination']
                    date = request.data['date']
                    date = datetime.strptime(date, '%Y-%m-%d %H:%M' )
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
                                user = User.objects.filter(id=user_id).first()
                                send_notification_email_task.apply_async(args=[user.name,user.email,flight_exists.date,flight_exists.origin,flight_exists.destination ], countdown=1)
                                return Response(serializer.data)
                        else:
                            return Response({'Message':'Seat already booked'})
                    return Response({'Message':'Flight doesnt exist'})
                return Response({'Message':'Invalid json keys'})
            return Response({'Message':'No token provided'})
        return Response({'Message':'Missing token key'})



class DetailsView(APIView):

    permission_classes = (permissions.AllowAny,)
    serializer_class = FlightSerializer

    def get(self, request, format=None):
        if 'HTTP_AUTHORIZATION' in list(request.META.keys()):
            if request.META['HTTP_AUTHORIZATION']:
                token = request.META['HTTP_AUTHORIZATION']
                user_id = Token.objects.values_list('user_id', flat=True).get(key=token)
                if user_id:
                    flights = Tickets.objects.filter(user_id=user_id).all()
                    serializer = FlightSerializer(flights, many=True)
                    return Response(serializer.data)
                else:
                    Response({'Message':'Invalid Token!'})
            return Response({'Message':'No token provided'})
        return Response({'Message':'Missing token key'})

