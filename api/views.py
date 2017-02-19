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
    queryset = models.UserProxy.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (IsOwnerOrPostOrReadOnly,)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class MessageViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend)
    ordering_fields = ('creation_time',)
    search_fields = ('content', 'created_by__username', 'created_by__first_name', 'created_by__last_name')
    filter_fields = ('created_by', 'room')
    ordering = ('-creation_time',)

    queryset = models.Message.objects.all()
    serializer_class = serializers.MessageSerializer
    permission_classes = (IsOwnerOrReadOnly,)
