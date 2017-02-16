from django.contrib.auth.models import User
from django.db import models


class UserProxy(User):
    class Meta:
        proxy = True

    def get_owner(self):
        return self


class Room(models.Model):
    name = models.CharField(max_length=200)
    creator = models.ForeignKey(UserProxy)
    creation_time = models.DateTimeField()
    radius = models.FloatField()
    expire_time = models.DateTimeField()
    image_url = models.CharField(max_length=500)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def get_owner(self):
        return self.creator
