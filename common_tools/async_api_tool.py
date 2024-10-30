
import requests

from common_tools.tools import async_task
from config.basic_setting import BASE_URL


@async_task
def update_mantis_graph(user_id, mode):
    """
    user_id: int
    mode: personal/all
    """
    request_params = {'user_id': user_id, 'update_mode': mode}
    url = BASE_URL + 'mantis/update/graph'
    requests.post(url, json=request_params)


@async_task
def update_mantis_single_graph(uuid, graph_id, graph_type):
    request_params = {'uuid': uuid, 'graph_id': graph_id, 'graph_type': graph_type}
    url = BASE_URL + 'mantis/update/single/graph'
    requests.post(url, json=request_params)
