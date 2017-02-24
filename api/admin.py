from django.contrib import admin
from api import models


class RoomAdmin(admin.ModelAdmin):
    pass


class MessageAdmin(admin.ModelAdmin):
    pass


class MembershipAdmin(admin.ModelAdmin):
    pass


class LikeAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Room, RoomAdmin)
admin.site.register(models.Message, MessageAdmin)
admin.site.register(models.Membership, MembershipAdmin)
admin.site.register(models.Like, LikeAdmin)
