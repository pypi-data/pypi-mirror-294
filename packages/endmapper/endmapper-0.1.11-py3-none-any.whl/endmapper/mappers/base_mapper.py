import json
import os.path as osp


class BaseEndpointMapper:
    @staticmethod
    def config():
        if osp.exists('emapcfg.json'):
            with open('emapcfg.json', 'r') as fp:
                obj = json.load(fp)
            return {
                'path_white_list': obj['path_white_list'] if 'path_white_list' in obj else [],
                'path_black_list': obj['path_black_list'] if 'path_black_list' in obj else [],
                'name_white_list': obj['name_white_list'] if 'name_white_list' in obj else [],
                'name_black_list': obj['name_black_list'] if 'name_black_list' in obj else [],
                'services': obj['services'] if 'services' in obj else [],
            }