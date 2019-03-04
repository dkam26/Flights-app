from django.db import models
from django.conf import settings


# Create your models here.
class Flight(models.Model):
    user = models.ForeignKey('user.User',
    related_name='flights',
    on_delete=models.CASCADE)
    origin = models.CharField(max_length=255, blank=False)
    destination = models.CharField(max_length=255, blank=False)
    flight_date =  models.DateTimeField()

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.origin)