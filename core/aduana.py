import requests

from config import config_object


def request_aduana(sucursal: str, manifiesto: str, awb: str):
    host = config_object.get('SERVER', 'HOST')
    endpoint = config_object.get('SERVER', 'ENDPOINT')
    response = requests.post(f'{host}/{endpoint}', json={'sucursal': sucursal, 'mnft': manifiesto, 'awb': awb})
    response.raise_for_status()
    return response.json()
