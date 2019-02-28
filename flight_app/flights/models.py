from django.db import models

# Create your models here.
class Flight(models.Model):
    origin = models.CharField(max_length=255, blank=False)
    destination = models.CharField(max_length=255, blank=False)
    flight_date =  models.DateTimeField()

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.origin)