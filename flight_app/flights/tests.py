from user.models import User
from .models import AvailableFlights, Tickets
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .serializers import ListFlightSerializer
from PIL import Image
import tempfile
import datetime

class ModelTestCase(TestCase):
    def setUp(self):
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        with open(tmp_file.name, 'rb') as data:
            self.user = {"name":"kamara", "password":"1234", "email":'gkam1989@gmail.com', "passport_photograh":data}
            self.client = APIClient()
            self.response = self.client.post(
                reverse('create'),
                self.user,
                format='multipart')
            res = self.client.post(
            reverse('login'),
            {'email':self.user['email'], 'password':self.user['password']},
            format='json')
            self.token = res.data['token']
        self.flight = {"id":1,"airline":"Kenyan airways",
                       "origin":"kampala",
                       "destination":"Nairobi",
                       "available_seats":30,
                       "date":"2019-03-04T14:34",
                       "plane_number":"43W",
                       "seats":{"seats":["1A","1B","1C","1D","1E","1F","2A","2B","2C","2D","2E","2F","3A","3B","3C","3D","3E","3F", "4A","4B","4C","4D","4E","4F", "5A","5B","5C","5D","5E","5F"]} }
        serialzer = ListFlightSerializer(data=self.flight)
        if serialzer.is_valid():
            serialzer.save()



    def test_available_flights(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(
            reverse('flights'),
            {'origin':"kampala", 'destination':"Nairobi"},
            format='json')
        self.assertIn('kampala', response.data[0].values())

    def test_available_flights_without_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.post(
            reverse('flights'),
            {'origin':"kampala", 'destination':"Nairobi","date":"datetime.now()},
            format='json')
        self.assertEqual(response.data, {'Message': 'No token provided'})


    # def test_user_can_book_flight(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=self.token)
    #     response = self.client.post(
    #         reverse('book flight'),
    #         {'origin':"kampala", 'destination':"Nairobi","date":"2019-03-04 14:34", "seat":"1A", "airline":"Kenyan airways"},
    #         format='json')
    #     self.assertEqual(response.data['airline'], 'Kenyan airways')

    def test_user_cant_book_flight_with_wrong_seat(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(
            reverse('book flight'),
            {'origin':"kampala", 'destination':"Nairobi","date":"2019-03-04 14:34", "seat":"AA", "airline":"Kenyan airways"},
            format='json')
        self.assertEqual(response.data, {'Message': 'Seat already booked'})

    def test_user_cant_book_flight_without_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.post(
            reverse('book flight'),
            {'origin':"kampala", 'destination':"Nairobi","date":"2019-03-04 14:34", "seat":"1A", "airline":"Kenyan airways"},
            format='json')
        self.assertEqual(response.data, {'Message': 'No token provided'})

    def test_user_cant_book_flight_that_doesnt_exist(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(
            reverse('book flight'),
            {'origin':"New york", 'destination':"Nairobi","date":"2019-03-04 14:34", "seat":"1A", "airline":"Kenyan airways"},
            format='json')
        self.assertEqual(response.data, {'Message': 'Flight doesnt exist'})