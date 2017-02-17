from api import models
from rest_framework import viewsets, permissions, filters
from api import serializers
from django_filters.rest_framework import DjangoFilterBackend


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


class UserViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend)
    ordering_fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    filter_fields = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    ordering = ('id',)

    queryset = models.UserProxy.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (IsOwnerOrPostOrReadOnly,)


class RoomViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend)
    ordering_fields = ('id', 'expire_time', 'creation_time', 'name')
    search_fields = ('name', 'created_by__username', 'created_by__first_name', 'created_by__last_name')
    filter_fields = ('id', 'name', 'created_by', 'longitude', 'latitude')
    ordering = ('id',)

    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class MessageViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend)
    ordering_fields = ('id', 'creation_time')
    search_fields = ('content', 'created_by__username', 'created_by__first_name', 'created_by__last_name')
    filter_fields = ('id', 'created_by', 'room')
    ordering = ('creation_time',)

    queryset = models.Message.objects.all()
    serializer_class = serializers.MessageSerializer
    permission_classes = (IsOwnerOrReadOnly,)
