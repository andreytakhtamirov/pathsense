import logging
import pickle

def load_pickle(blob_service_client, container_name, file_name):
    try:
        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob=file_name)
        blob_data = blob_client.download_blob().readall()

        obj = pickle.loads(blob_data)
        return obj
    except:
        logging.info(f'Exception during: {file_name}')
