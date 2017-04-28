from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.conf import settings
from pyfcm import FCMNotification
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


fcm_api_key = getattr(settings, 'FCM_API_KEY', '')
push_service = FCMNotification(api_key=fcm_api_key) if fcm_api_key != '' else None


@receiver(models.signals.post_save, sender=Message)
def execute_after_save(sender, instance: Message, created, *args, **kwargs):
    if push_service is not None:
        for membership in Membership.objects.filter(room=instance.room).exclude(user=instance.created_by).all():
            for device in Device.objects.filter(user=membership.user).all():
                push_service.notify_single_device(
                    registration_id=device.device,
                    message_title=instance.room.name,
                    message_body=instance.content,
                    data_message={
                        'Id': instance.room.id,
                        'Title': instance.room.name,
                        'Message': instance.content,
                        'Sender': instance.created_by.username
                    }
                )


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


class Device(models.Model):
    user = models.ForeignKey(UserProxy, on_delete=models.CASCADE)
    device = models.CharField(max_length=2048)

    class Meta:
        unique_together = ['user', 'device']

    def get_owner(self):
        return self.user

    def __str__(self):
        return "{}'s device".format(self.user)
