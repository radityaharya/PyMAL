import json

def reform_json(data)->list:
    list_of_dicts = []
    for item in data['data']:
        list_of_dicts.append(item['node'])
    return list_of_dicts