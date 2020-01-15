from rest_framework.views import APIView 
from django.http import Http404
from rest_framework import status 
from rest_framework.response import Response
from rest_framework import generics, filters
from django.contrib.gis.geos import fromstr, Point
from django.contrib.gis.db.models.functions import Distance
import requests
from . models import PlacesModel, WebPagesModel, ServicesModel, CarusselModel
from .serializers import PlacesSerializer, WebPagesSerializer, CarusselSerializer,ServicesSerializer


class PlacesList(generics.ListCreateAPIView):
    filter_backends = [filters.SearchFilter]
    search_fields = ['cartegory', 'name']
    queryset = PlacesModel.objects.all() 
    serializer_class = PlacesSerializer
    paginate_by = 8


class PlaceDetail(generics.RetrieveDestroyAPIView):
    queryset = PlacesModel.objects.all()
    serializer_class =PlacesSerializer


class MyPlacesList(generics.ListCreateAPIView):
    serializer_class = PlacesSerializer

    def get_queryset(self):
        """
        This view should return a list of all the places
        for the currently authenticated user.
        """
        user = self.request.user
        if user == AnonymousUser:
            user = 1
        return PlacesModel.objects.filter(created_by=user)
    
    def perform_create(self, serializer): 

        serializer.save(created_by=self.request.user)
        return serializer.data


class MyPlacesDetail(generics.RetrieveDestroyAPIView):
    serializer_class = PlacesSerializer
    
    def get_queryset(self):
        
        
        queryset = PlacesModel.objects.filter(places_id=self.kwargs["pk"])
        return queryset



class NearestPlacesList(generics.ListAPIView):

    """returns list of all the resisdentials nearest 
    to the user location and supports search 
    by 'tittle', 'email', and 'user name or created by' """
    

    def get_queryset(self, request):

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
        response = requests.get('http://freegeoip.net/json/%s' % ip_address)
        geodata = response.json()
        latitude = geodata['latitude']
        longitude = geodata['longitude']
        user_location = Point(longitude, latitude, srid=4326)

        return PlacesModel.objects.annotate(
        distance=Distance('location',user_location)).order_by('distance') #[0:6]

    filter_backends = [filters.SearchFilter]
    search_fields = ['cartegory', 'name']

    # queryset = PlacesModel.objects.all() 
    serializer_class = PlacesSerializer
    paginate_by = 8

    
class NearestPlacesDetail(generics.RetrieveDestroyAPIView):
    def get_queryset(self, request):

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
        response = requests.get('http://freegeoip.net/json/%s' % ip_address)
        geodata = response.json()
        latitude = geodata['latitude']
        longitude = geodata['longitude']
        user_location = Point(longitude, latitude, srid=4326)

        return PlacesModel.objects.annotate(
            distance=Distance('location',user_location)).order_by('distance')
    serializer_class = PlacesSerializer







# web pages



class WebPagesList(generics.ListCreateAPIView):
    """ returns webpages for a specific registered place """
    def get_queryset(self): 
        queryset = WebPagesModel.objects.filter(places_id=self.kwargs["pk"]) 
        return queryset 
    
    serializer_class = WebPagesSerializer

class WebPageDetail(generics.RetrieveDestroyAPIView):
    """ returns details of a webpage For a specific registered places"""

    def get_queryset(self): 
        try:
            queryset = WebPagesModel.objects.get(pk=self.kwargs["webpage_pk"]) 
            return queryset 
        except WebPagesModel.DoesNotExist:
            raise Http404

    serializer_class = WebPagesSerializer


class WebPagesList(generics.ListCreateAPIView):

    """ 
        returns all webpages for registered places with search option
        all can view but read only
    """

    filter_backends = [filters.SearchFilter]
    search_fields = ['tittle', 'place']
    queryset = WebPagesModel.objects.all()
    serializer_class = WebPagesSerializer

class WebPageDetail(generics.RetrieveDestroyAPIView):
    """ 
        returns details of a webpage For  specific registered places
        all can view but read only
    """

    queryset = WebPagesModel.objects.all()
    serializer_class = WebPagesSerializer











# web page services section


class CreateService(APIView):
    serializer_class = ServicesSerializer
    
    def post(self, request, webpage_pk):
        "create a service for a webpage"

        service = request.data.get("service")
        data =  {'service':service, 'webpage':webpage_pk}
        serializer = ServicesSerializer(data=data)

        if serializer.is_valid:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get (self, webpage_pk, request):
        "get services of a webpage"

        services = ServicesModel.objects.filter(webpages_id= webpage_pk)
        serializer = ServicesSerializer(services, many=True)
        return response(serializer.data)


class UpdateService(APIView):

    serializer_class = ServicesSerializer

    def get_object(self, service_pk):
        try:
            return ServicesModel.objects.get(pk=service_pk)
        except ServicesModel.DoesNotExist:
            raise Http404

    def get(self, request, service_pk):

        pk = service_pk
        service = self.get_object(pk)
        serializer = ServicesSerializer(service)
        return Response(serializer.data)

    def put(self, request, service_pk ):
        service = self.get_object(pk=service_pk)
        serializer = ServicesSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, service_pk, format=None):
        service = self.get_object(pk=service_pk)
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

















# web page carussel section


class CreateCarussel(APIView):
    serializer_class = CarusselSerializer
    
    def post(self, request, webpage_pk):

        image = request.data.get("image")
        data =  {'image':image, 'webpage':webpage_pk }
        serializer = CarusselSerializer(data=data)

        if serializer.is_valid:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get (self, webpage_pk, request):

        carussel = CarusselModel.objects.filter(webpages_id= webpage_pk)
        serializer = CarusselSerializer(carussel, many=True)
        return response(serializer.data)


class UpdateCarussel(APIView):

    serializer_class = CarusselSerializer

    def get_object(self, carussel_pk):
        try:
            return CarusselModel.objects.get(pk=carussel_pk)
        except CarusselModel.DoesNotExist:
            raise Http404

    def get(self, request, carussel_pk):

        pk = carussel_pk
        carussel = self.get_object(carussel_pk)
        serializer = CarusselSerializer(carussel)
        return Response(carussel.data)

    def put(self, request, carussel_pk ):
        carussel = self.get_object(pk=carussel_pk)
        serializer = CarusselSerializer(carussel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, carussel_pk, format=None):
        service = self.get_object(pk=carussel_pk)
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
















