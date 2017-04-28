from rest_framework.authtoken.models import Token

from api import models
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.UserProxy
        fields = (
            'url',
            'username',
            'email',
            'is_staff',
            'first_name',
            'last_name',
            'date_joined',
            'password',
        )
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'date_joined': {'read_only': True},
            'is_staff': {'read_only': True},
        }

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super(UserSerializer, self).update(instance, validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
            Token.objects.filter(user_id=user.id).delete()
        user.save()
        return user


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Room
        fields = '__all__'
        extra_kwargs = {
            'creation_time': {'read_only': True},
            'created_by': {'read_only': True, 'default': serializers.CurrentUserDefault()}
        }


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Message
        fields = '__all__'
        extra_kwargs = {
            'creation_time': {'read_only': True},
            'created_by': {'read_only': True, 'default': serializers.CurrentUserDefault()},
        }


class MembershipSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Membership
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True, 'default': serializers.CurrentUserDefault()},
        }


class LikeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Like
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True, 'default': serializers.CurrentUserDefault()},
        }


class LikeRoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.LikeRoom
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True, 'default': serializers.CurrentUserDefault()},
        }


class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Device
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True, 'default': serializers.CurrentUserDefault()},
        }
