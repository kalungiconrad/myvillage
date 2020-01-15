# from django.shortcuts import render
from rest_framework import generics, filters
from . serializers import UserProfileSerializer
from . models import UserProfileModel
# Create your views here.


class UserList(generics.ListCreateAPIView): 
    
    queryset = UserProfileModel.objects.all()
    serializer_class = UserProfileSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfileModel.objects.all()
    serializer_class = UserProfileSerializer

# class Cartegories(generics.GenericListAPIView): # new
#     queryset = UserProfileModel.objects.all()
    

#     def get(self, request, *args, **kwargs):
#         user = self.get_object()
#         data = {'cartegory':user.Cartegories}
#         return JsonResponse(data)

class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user)