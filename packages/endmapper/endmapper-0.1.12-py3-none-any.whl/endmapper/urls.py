from django.urls import path
from endmapper.mappers.dj_mapper import DjangoEndpointMapper

urlpatterns = [
    path('api/endpoint/', DjangoEndpointMapper.as_view())
]