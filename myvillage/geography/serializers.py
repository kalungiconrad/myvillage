from rest_framework import serializers


from . models import  GeographyModel

class GeographySerializer( serializers.ModalSerializer):
    
    class Meta:
        model = GeographyModel
        fields = '__all__'
        #read_only_fields = ['']