from django.contrib.auth.models import User
from django.db import models
from .distance_manager import WithDistanceManager


class UserProxy(User):
    class Meta:
        proxy = True

    def get_owner(self):
        return self


class Room(models.Model):
    objects = WithDistanceManager()

    name = models.CharField(max_length=200)
    created_by = models.ForeignKey(UserProxy, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    radius = models.FloatField()
    expire_time = models.DateTimeField(null=True)
    image_url = models.CharField(max_length=500, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    members = models.ManyToManyField(UserProxy, through='Membership', related_name='+')

    def get_owner(self):
        return self.created_by

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(UserProxy, on_delete=models.CASCADE)
    anonymous = models.BooleanField()
    content = models.CharField(max_length=1024)
    likes = models.ManyToManyField(UserProxy, through='Like', related_name='+')

    def get_owner(self):
        return self.created_by

    def __str__(self):
        return "{}: {}".format(self.created_by.username, self.content)


class Membership(models.Model):
    user = models.ForeignKey(UserProxy, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    muted = models.BooleanField()

    def get_owner(self):
        return self.user

    def __str__(self):
        return "{} in {}".format(self.user, self.room)


class Like(models.Model):
    user = models.ForeignKey(UserProxy, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)

    def get_owner(self):
        return self.user

    def __str__(self):
        return "{} liked {}".format(self.user, self.message)

class LikeRoom(models.Model):
    user = models.ForeignKey(UserProxy, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def get_owner(self):
        return self.user

    def __str__(self):
        return "{} liked {}".format(self.user, self.room)