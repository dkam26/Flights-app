from django.test import TestCase
import datetime
# Create your tests here.
from .models import Flight
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from user.models import User
from django.utils import timezone

class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(name="kamara", password='1234', email='kd@gmail.com')
        self.client = APIClient()
        self.origin =  'Kampala'
        self.destination = 'Boston'
        self.flight_date = datetime.datetime.now()
        self.flight_data = {'user':self.user.id, 'origin': self.origin, 'destination': self.destination, 'flight_date': timezone.now()}
        self.response = self.client.post(
            reverse('create'),
            self.flight_data,
            format="json")

    def test_model_can_book_a_flight(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)


    def test_api_can_delete_flight(self):
        flight = Flight.objects.get()
        response = self.client.delete(
            reverse('details', kwargs={'pk': flight.id}),
            format='json',
            follow=True)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_api_can_get_a_bucketlist(self):
        flight = Flight.objects.get()
        response = self.client.get(
            reverse('details', kwargs={'pk': flight.id}),
            format='json',
            follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, flight)

    def test_api_can_update_bucketlist(self):
        flight = Flight.objects.get()
        change_flight_data = {'user':self.user.id, 'origin': 'Chicago', 'destination': 'Cuba', 'flight_date': timezone.now()}
        res = self.client.put(
            reverse('details', kwargs={'pk': flight.id}),
            change_flight_data, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
