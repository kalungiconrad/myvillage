from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import  MyPlacesList, MyPlacesDetail,  WebPagesList,  WebPageDetail, CreateService, UpdateService, CreateCarussel, UpdateCarussel, NearestPlacesList,  NearestPlacesDetail

urlpatterns = [ 
   
    path('', MyPlacesList.as_view(), name="my-places-list"),
    path('<int:pk>/', MyPlacesDetail.as_view(), name="my-places-detail"),  
    path('<int:pk>/webpage/', WebPagesList.as_view(), name="webpages-list"),  
    path('<int:pk>/webpage/<int:webpage_pk>/', WebPageDetail.as_view(), name="webpage-detail"),  
    path('<int:pk>/webpage/<int:webpage_pk>/service/', CreateService.as_view(), name="services-list"),  
    path('<int:pk>/webpage/<int:webpage_pk>/service/<int:service_pk>/', UpdateService.as_view(), name="service-detail"),  
    path('<int:pk>/webpage/<int:webpage_pk>/carussel/', CreateCarussel.as_view(), name="carussel-list"),  
    path('<int:pk>/webpage/<int:webpage_pk>/carussel/<int:carussel_pk>/', UpdateCarussel.as_view(), name="carussel-detail"),  

    path('nearest-places',  NearestPlacesList.as_view()),
    path('nearest-places/<int:pk>', NearestPlacesDetail.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)