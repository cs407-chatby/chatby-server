from django.contrib.auth.models import User


class UserProxy(User):

    class Meta:
        proxy = True

    def get_owner(self):
        return self
