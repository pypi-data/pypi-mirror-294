from django.urls import get_resolver, path
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class EndpointMapperView(APIView):
    @staticmethod
    def get(response):
        result = EndpointMapper(path_white_list=['api'], name_black_list=['schema'],
                                microservices={
                                    "communicator": "http://communicator-app-1:8000/api/search/endpoints/"}).result
        return Response(result, status=status.HTTP_200_OK)


class EndpointMapper:
    def __init__(self, path_white_list=None, path_black_list=None, name_white_list=None, name_black_list=None, microservices=None):
        self.result = {}
        self.path_white_list = path_white_list if path_white_list is not None else []
        self.path_black_list = path_black_list if path_black_list is not None else []
        self.name_white_list = name_white_list if name_white_list is not None else []
        self.name_black_list = name_black_list if name_black_list is not None else []
        self.microservices = microservices if microservices and isinstance(microservices, dict) else {}

        if any(w_point in self.path_black_list for w_point in self.path_white_list):
            raise Exception('Black and white path lists cannot have the same values')
        if any(w_point in self.name_black_list for w_point in self.name_white_list):
            raise Exception('Black and white name lists cannot have the same values')

        urlpattern = get_resolver().url_patterns

        for i, item in enumerate(urlpattern):
            urls_list = self.get_urls(item)
            if not urls_list:
                continue

            for key, value in urls_list.items():
                self.result[key] = value

    def get_urls(self, item, parent_url=''):
        result = {}

        endpoint = str(item.pattern)

        if hasattr(item, 'url_patterns'):
            for pattern in item.url_patterns:
                urls_list = self.get_urls(pattern, parent_url + endpoint)
                if not urls_list:
                    continue

                for key, value in urls_list.items():
                    if value is None:
                        del result[key]
                    else:
                        result[key] = value
        else:
            while True:
                name = parent_url + endpoint

                if not item.name:
                    print(f'No url patterns found for {name}')
                    break

                if item.name in self.microservices.keys():
                    response = requests.get(self.microservices[item.name])
                    print(response)
                    break

                if len(self.name_white_list) > 0 and not any(point in item.name for point in self.name_white_list):
                    break
                elif len(self.name_black_list) > 0 and any(point in item.name for point in self.name_black_list):
                    break
                elif len(self.path_white_list) > 0 and not any(name.startswith(point) for point in self.path_white_list):
                    break
                elif len(self.path_black_list) > 0 and any(name.startswith(point) for point in self.path_black_list):
                    break

                result[item.name] = name
                break

        return result