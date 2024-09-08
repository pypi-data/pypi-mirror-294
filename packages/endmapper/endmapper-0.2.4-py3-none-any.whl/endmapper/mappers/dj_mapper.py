from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from endmapper.mappers.base_mapper import BaseEndpointMapper
from endmapper import endpoint_handlers


class DjangoEndpointMapper(APIView):
    """
    ATTENTION: add "path("", include("endmapper.urls"))" to main urls

    This will add new endpoint "api/endpoints/" to your project
    """
    @staticmethod
    def get(response):
        config = BaseEndpointMapper.config()
        print(config)
        result = endpoint_handlers.DjangoEndpointHandler(**config).result
        return Response(result, status=status.HTTP_200_OK)

# path_white_list=['api'], name_black_list=['schema'],
#                                 microservices={
#                                     "communicator": "http://communicator-app-1:8000/api/search/endpoints/"}

