import os

account_name = os.environ['BLOB_STORAGE_ACCOUNT_NAME']
account_key = os.environ['BLOB_STORAGE_ACCOUNT_KEY']

CONNECTION_STRING = f'DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net'
CONTAINER_NAME = 'graph-pickles'
BLOB_NAME = 'waterloo_40km.pickle'
