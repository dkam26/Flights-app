from rest_framework import generics
from .models import Flight
from .serializers import FlightSerializer
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from flight_app.settings import SECRET_KEY
from rest_framework.authtoken.models import Token
from django.core import serializers
class CreateView(APIView):
    serializer_class = FlightSerializer
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        if request.META['HTTP_AUTHORIZATION']:
            token = request.META['HTTP_AUTHORIZATION']
            user_id = Token.objects.values_list('user_id', flat=True).get(key=token)
            flight_data = request.data
            flight_data['user'] = user_id
            flight = Flight.objects.filter(origin=flight_data['origin'],destination=flight_data['destination'],flight_date=flight_data['flight_date'],user_id=flight_data['user']).exists()
            if not flight:
                serializer = FlightSerializer(data=flight_data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data)
            return Response('Flight exists')
        return Response('No token provided')



class DetailsView(APIView):

    permission_classes = (permissions.AllowAny,)
    serializer_class = FlightSerializer

    def get(self, request, format=None):
        flight_data = {}
        index = 0
        if request.META['HTTP_AUTHORIZATION']:
            token = request.META['HTTP_AUTHORIZATION']
            user_id = Token.objects.values_list('user_id', flat=True).get(key=token)
            flights = Flight.objects.filter(user_id=user_id).all()
            return Response(serializers.serialize('json', flights))
        return Response('No token provided')