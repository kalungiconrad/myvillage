from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.UserList.as_view()),
    path('<int:pk>/', views.UserDetail.as_view() ),
    # path('<int:pk>/cartegories/',
    #      views.Cartegories.as_view(), name='cartegories')
    

]

urlpatterns = format_suffix_patterns(urlpatterns)