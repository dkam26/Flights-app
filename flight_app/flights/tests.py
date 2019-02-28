from django.test import TestCase

# Create your tests here.
from .models import Flight
import datetime

class ModelTestCase(TestCase):
    def setUp(self):

        self.origin = 'Kampala'
        self.destination = 'Boston'
        self.flight_date = datetime.datetime.now()
        self.flight = Flight(origin=self.origin, destination=self.destination, flight_date = self.flight_date)

    def test_model_can_create_a_bucketlist(self):
        old_count = Flight.objects.count()
        self.flight.save()
        new_count = Flight.objects.count()
        self.assertNotEqual(old_count, new_count)