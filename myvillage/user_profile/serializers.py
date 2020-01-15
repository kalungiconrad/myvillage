from rest_framework import serializers
from . import models
from places.models import PlacesModel
class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    """ a serializer for  "user profile" objects"""
    places  = serializers.HyperlinkedRelatedField(
        many=True,
        # read_only=True,
        view_name='my-places-list',
        queryset= PlacesModel.objects.all()
    )

    class Meta:
        model = models.UserProfileModel
        fields = ('id','email','first_name','last_name','password','avatar', 'places')

        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """create and return user"""
        user = models.UserProfileModel(
            email = validated_data['email'],
            first_name= validated_data['first_name'],
            last_name = validated_data['last_name'],
            avatar = validated_data['avatar']
        )
        user.set_password(validated_data['password']) 
        user.save()
        return user
