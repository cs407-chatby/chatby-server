from django.db.models import F

from api import models
from rest_framework import viewsets, permissions, filters
from api import serializers
from django_filters.rest_framework import DjangoFilterBackend

from decimal import Decimal


class IsOwnerOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        try:
            return request.user.is_authenticated and \
                   obj.get_owner() == request.user
        except AttributeError:
            return False


class IsOwnerOrPostOrReadOnly(IsOwnerOrReadOnly):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return super(IsOwnerOrPostOrReadOnly, self).has_permission(request, view)


class IsCreatorOrOwnerOrReadOnly(IsOwnerOrReadOnly):
    def has_object_permission(self, request, view, obj):
        is_owner = super(IsCreatorOrOwnerOrReadOnly, self).has_object_permission(request, view, obj)
        authenticated = request.user.is_authenticated
        is_creator = authenticated and (obj.room.created_by == request.user)
        return is_owner or is_creator


class IsMemberAndOwnerOrReadOnly(IsOwnerOrReadOnly): # TODO make this work for POST too
    def has_object_permission(self, request, view, obj):
        is_owner = super(IsMemberAndOwnerOrReadOnly, self).has_object_permission(request, view, obj)
        authenticated = request.user.is_authenticated
        is_member = authenticated and (models.Membership.objects.filter(user= request.user, room= obj.room).exists())
        is_safe = request.method in permissions.SAFE_METHODS
        return is_safe or (is_owner and is_member)


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.UserProxy.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (IsOwnerOrPostOrReadOnly,)

    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk == 'current' and self.request.user.is_authenticated:
            return self.request.user
        return super(UserViewSet, self).get_object()


class RoomViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('created_by',)
    serializer_class = serializers.RoomSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    @staticmethod
    def __as_float_or_none(value):
        try:
            return float(round(Decimal(value), 5))
        except (ValueError, TypeError):
            return None

    def get_queryset(self):
        objects = models.Room.objects
        latitude = self.__as_float_or_none(self.request.query_params.get('my_lat', None))
        longitude = self.__as_float_or_none(self.request.query_params.get('my_lon', None))
        if latitude is not None and longitude is not None:
            return objects.with_distance(latitude, longitude).filter(distance__lt=F('radius')).all()
        else:
            return objects.all()


class MessageViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend)
    ordering_fields = ('creation_time',)
    search_fields = ('content', 'created_by__username', 'created_by__first_name', 'created_by__last_name')
    filter_fields = ('created_by', 'room')
    ordering = ('-creation_time',)

    queryset = models.Message.objects.all()
    serializer_class = serializers.MessageSerializer
    permission_classes = (IsMemberAndOwnerOrReadOnly,)


class MembershipViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user', 'room')

    queryset = models.Membership.objects.all()
    serializer_class = serializers.MembershipSerializer
    permission_classes = (IsCreatorOrOwnerOrReadOnly,)


class LikeViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user', 'message')

    queryset = models.Like.objects.all()
    serializer_class = serializers.LikeSerializer
    permission_classes = (IsOwnerOrReadOnly,)
