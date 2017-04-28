from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken import views as auth_views
from api import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'rooms', views.RoomViewSet, base_name='room')
router.register(r'messages', views.MessageViewSet)
router.register(r'memberships', views.MembershipViewSet)
router.register(r'likes', views.LikeViewSet)
router.register(r'roomlikes', views.LikeRoomViewSet)
router.register(r'devices', views.DeviceViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', auth_views.obtain_auth_token),
    url(r'^session-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
