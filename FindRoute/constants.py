import os

account_name = os.environ['BLOB_STORAGE_ACCOUNT_NAME']
account_key = os.environ['BLOB_STORAGE_ACCOUNT_KEY']

CONNECTION_STRING = f'DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net'
CONTAINER_NAME = 'graph-gravel-cycling'
BLOB_NAME_COORDS_DICTIONARY = 'dict_coords.pickle'
GRAPH_PICKLE_FILE_NAME = 'graph_{}_{}.pickle'
TILE_DIMENSION_RADIUS = 10000

ERROR_MESSAGE_INVALID_COORDINATES = 'Invalid input coordinates.'

NUM_ROUTES_TO_BUILD = 2 # Will generate 1 main route and 1 alternative route.
