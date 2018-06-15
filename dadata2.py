# -*- coding: utf-8 -*-
import json
import requests

api_dadata = "4ea6a07834e4edf11752f20c348cff623c0021ea"
BASE_URL = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/%s'


def suggest(query, resource):
    url = BASE_URL % resource
    headers = {
        'Authorization': 'Token %s' % api_dadata,
        'Content-Type': 'application/json',
    }
    data = {
        'query': query
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    data = r.json()
    if not data['suggestions']:
        return None

    return data['suggestions'][0]['value'], data['suggestions'][0]['data']['management']['post'], \
           data['suggestions'][0]['data']['management']['name'], data['suggestions'][0]['data']['address']['value']



