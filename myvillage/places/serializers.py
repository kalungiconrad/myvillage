from rest_framework import serializers
# from rest_framework_gis.serializers import GeoFeatureModelSerializer

from places.models import PlacesModel, WebPagesModel, ServicesModel, CarusselModel

class PlacesSerializer(serializers.ModelSerializer):
    webpage = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="webpage-list",
        queryset = WebPagesModel.objects.all()
    )
    class Meta:
        model = PlacesModel
        fields = ['name','image','created_by', 'contact', 'email', 'cartegory','webpage' ]
        read_only_fields = ['created_by']


class WebPagesSerializer(serializers.ModelSerializer):
    services = serializers.HyperlinkedRelatedField(
        many=True,
        view_name = "services-list",
        queryset = ServicesModel.objects.all()
    )
    Carussel = serializers.HyperlinkedRelatedField(
        many=True,
        view_name = "carussel-list",
        queryset = CarusselModel.objects.all()
    )
    class Meta:
        model = WebPagesModel
        fields = ['tittle','subtittle','about_us','footer','place','created', 'services','carussel']
        read_only_fields = ['location','created']

    

class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicesModel
        fields = ['service','webpage']
        read_only_fields = ['webpage']


class CarusselSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarusselModel
        fields = ['image','webpage']
        read_only_fields = ['webpage']




 