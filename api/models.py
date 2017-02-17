from django.contrib.auth.models import User
from django.db import models


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

    def get_owner(self):
        return self.created_by


class Message(models.Model):
    created_by = models.ForeignKey(UserProxy, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=1024)
