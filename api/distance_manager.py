from django.db import models
from django.db.models import F, Func
from django.db.backends.signals import connection_created
from django.dispatch import receiver
import math


@receiver(connection_created)
def extend_sqlite(connection=None, **kwargs):
    if connection.vendor == "sqlite":
        # sqlite doesn't natively support math functions, so add them
        cf = connection.connection.create_function
        cf('SIN', 1, math.sin)
        cf('COS', 1, math.cos)
        cf('ACOS', 1, math.acos)
        cf('RADIANS', 1, math.radians)


class WithDistanceManager(models.Manager):
    def with_distance(self, latitude, longitude):
        """
        Returns a QuerySet of locations annotated with their distance from the
        given point. This can then be filtered.
        Usage:
            Foo.objects.with_distance(lat, lon).filter(distance__lt=10).count()
        @see http://stackoverflow.com/a/31715920/1373318
        """

        # noinspection PyAbstractClass
        class Sin(Func):
            function = 'SIN'

        # noinspection PyAbstractClass
        class Cos(Func):
            function = 'COS'

        # noinspection PyAbstractClass
        class Acos(Func):
            function = 'ACOS'

        # noinspection PyAbstractClass
        class Radians(Func):
            function = 'RADIANS'

        given_lat = Radians(latitude)  # given latitude
        given_lon = Radians(longitude)  # given longitude
        my_lat = Radians(F('latitude'))
        my_lon = Radians(F('longitude'))

        # Note 3959.0 is for miles. Use 6371 for kilometers
        expression = 3959.0 * Acos(Cos(given_lat) * Cos(my_lat) *
                                   Cos(my_lon - given_lon) +
                                   Sin(given_lat) * Sin(my_lat))

        return self.get_queryset() \
            .exclude(latitude=None) \
            .exclude(longitude=None) \
            .annotate(distance=expression)
