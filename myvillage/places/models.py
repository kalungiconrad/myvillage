from geography.models import GeographyModel
from user_profile.models import UserProfileModel
from django.db import models
# Create your models here.


class PlacesManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name )

class PlacesModel(GeographyModel):
    Cartegories = (
        ("RESIDENTIALS","residentials"),("EDUCATION","education"),
        ("HEALTH","health"),("HOSPITALITY","hospitality"),
        ("SPORTS","sports"),("ART","art"),("FARM","farm"),
        ("OFFICES","offices"),("SHOPS","shops"),
        ("SERVICES","services"),
        )

    places_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)  
    image = models.ImageField(upload_to='images', null=True, blank=True)
    created_by = models.ForeignKey(UserProfileModel, related_name = 'places', on_delete=models.CASCADE)
    contact = models.CharField(max_length=13, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    cartegory = models.CharField(blank=False, choices=Cartegories, max_length=20 )
    
    objects = PlacesManager()

    def __str__(self):
        return self.name

    
class WebPagesManager(models.Manager):
    def get_by_natural_key(self, tittle):
        return self.get(tittle=tittle )

class WebPagesModel(models.Model):

    webpages_id = models.AutoField(primary_key=True)
    # tittle = models.CharField(max_length=100, unique =True, blank=False)
    tittle = models.CharField(max_length=100, unique=True, blank=False)
    subtittle = models.CharField(max_length=120, null=True)
    about_us = models.CharField(max_length=300, null=True)
    footer = models.CharField(max_length=100, null=True)
    place = models.OneToOneField(PlacesModel, on_delete=models.CASCADE, related_name="webpage")
    created = models.DateTimeField( auto_now_add=True)

    objects = WebPagesManager()

    def __str__(self):
        return self.tittle




class ServicesModel(models.Model):

    services_id = models.AutoField(primary_key=True)
    service = models.CharField(max_length=100, blank=False, unique=True)
    webpage = models.ForeignKey(WebPagesModel, on_delete=models.CASCADE, related_name="services")
    
    def __str__(self):
        return self.service

class CarusselModel(models.Model):

    carussel_id = models.AutoField(primary_key=True)
    image = models.ImageField(null=True, upload_to="carussel")
    webpage = models.ForeignKey(WebPagesModel, on_delete=models.CASCADE, related_name="carussel")

    def __str__(self):
        return self.image