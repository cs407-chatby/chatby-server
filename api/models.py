from django.contrib.auth.models import User
from django.db import models
from django.contrib.gis.db import models as gis_models

class UserProxy(User):
    class Meta:
        proxy = True

    def get_owner(self):
        return self


class Room(models.Model):
    name = models.CharField(max_length=200)
    created_by = models.ForeignKey(UserProxy, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    radius = models.FloatField()
    expire_time = models.DateTimeField(null=True)
    image_url = models.CharField(max_length=500, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    # location = gis_models.PointField()

    def get_owner(self):
        return self.created_by

    def __str__(self):
        return self.name


class Message(models.Model):
    created_by = models.ForeignKey(UserProxy, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=1024)

    def get_owner(self):
        return self.created_by

    def __str__(self):
        return "{}: {}".format(self.created_by.username, self.content)
