import logging

import azure.functions as func
from azure.storage.blob import BlobServiceClient
import osmnx as ox
from FindRoute.constants import BLOB_NAME, CONNECTION_STRING, CONTAINER_NAME

from gravel_cycling.weight import cycle_gravel_edge_weight
from convert.polyline import route_to_polyline6
import pickle
import json


blob_service_client = BlobServiceClient.from_connection_string(
    CONNECTION_STRING)

blob_client = blob_service_client.get_blob_client(
    container=CONTAINER_NAME, blob=BLOB_NAME)
blob_data = blob_client.download_blob().readall()

G = pickle.loads(blob_data)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()

        origin = req_body['origin']
        destination = req_body['destination']

        start_node = ox.nearest_nodes(
            G, origin['longitude'], origin['latitude'])
        end_node = ox.nearest_nodes(
            G, destination['longitude'], destination['latitude'])

        route = ox.shortest_path(G, start_node, end_node,
                                 weight=cycle_gravel_edge_weight)

        response_body = {
            "routes": [
                {
                    "geometry": route_to_polyline6(G, route)
                }
            ]
        }
        return func.HttpResponse(json.dumps(response_body),
                                 status_code=200,
                                 mimetype="application/json"
                                 )

    except ValueError as e:
        logging.error(f'Invalid request: {e}')
        return func.HttpResponse(body='Invalid request', status_code=400)

    except Exception as ex:
        logging.error(f'Exception: {ex}')
        return func.HttpResponse(body='Internal server error', status_code=500)
