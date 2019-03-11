# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from django.conf import settings
from django.contrib.postgres.fields import JSONField



class AvailableFlights(models.Model):
    airline = models.CharField(max_length=255, blank=True, null=True)
    origin = models.CharField(max_length=255, blank=True, null=True)
    destination = models.CharField(max_length=50, blank=True, null=True)
    available_seats = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    plane_number = models.CharField(max_length=50, blank=True, null=True)
    seats = JSONField()

    class Meta:
        managed = False
        db_table = 'available_flights'


class Tickets(models.Model):
    airline = models.CharField(max_length=50, blank=True, null=True)
    origin = models.CharField(max_length=50, blank=True, null=True)
    destination = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    plane_number = models.CharField(max_length=50, blank=True, null=True)
    seat_number = models.CharField(max_length=50, blank=True, null=True)
    user = models.ForeignKey('user.User',
    related_name='flights',
    on_delete=models.CASCADE)

    def __str__(self):
        return self.plane_number

