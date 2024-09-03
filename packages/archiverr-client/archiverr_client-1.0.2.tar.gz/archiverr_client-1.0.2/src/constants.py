from types import MappingProxyType
_constants = {
    'API_KEY': 'your_api_key_here',
    'MAX_RETRIES': 5,
    'TIMEOUT': 30
}

CONSTANTS = MappingProxyType(_constants)
