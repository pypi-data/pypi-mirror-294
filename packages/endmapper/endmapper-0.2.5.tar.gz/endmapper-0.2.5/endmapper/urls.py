from django.urls import path
from endmapper.mappers.dj_mapper import DjangoEndpointMapper

urlpatterns = [
    path('api/endpoints/', DjangoEndpointMapper.as_view())
]