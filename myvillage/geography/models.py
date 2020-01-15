from django.contrib.gis.db import models

# Create your models here.
class GeographyModel(models.Model):
    location = models.PointField(null=False, blank=False)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.location