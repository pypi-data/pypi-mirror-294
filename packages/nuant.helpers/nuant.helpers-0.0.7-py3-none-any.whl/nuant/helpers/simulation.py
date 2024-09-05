import requests
import gzip
import json
from io import BytesIO
import datetime


def __get_nuant_api_url(api_url: str) -> str:
    if api_url:
        return api_url
    elif __builtins__.get('NUANT_CONTEXT') and NUANT_CONTEXT.API_URL:
        return NUANT_CONTEXT.API_URL
    else:
        raise Exception("You need to provide the Nuant API url")


def __get_headers(api_key: str) -> dict:
    headers = {
        'Content-Type': 'application/json'
    }

    if api_key:
        headers['x-api-key'] = api_key
    elif __builtins__.get('NUANT_CONTEXT') and NUANT_CONTEXT.API_KEY:
        headers['x-api-key'] = NUANT_CONTEXT.API_KEY
    elif __builtins__.get('NUANT_CONTEXT') and NUANT_CONTEXT.JWT:
        headers['Authorization'] = f"{NUANT_CONTEXT.JWT}"
    else:
        raise Exception("You need to provide an authorization method")

    return headers


def fetch_data(simulation_id: str, file: str, api_key: str ='', api_url: str ="https://data.ptn.cobrabreiz.services/graphql"):
    try:
        list_files = fetch_list_files(simulation_id, api_key, api_url)

        result_link = list_files[file]

        response_file = requests.request("GET", result_link)

        buffer_data = BytesIO(response_file.content)

        result_file = gzip.GzipFile(fileobj=buffer_data).read()

        return json.loads(result_file)
    except Exception as e:
        print("An exception occurred: %s" % repr(e))


def fetch_list_files(simulation_id: str, api_key: str ='', api_url: str ="https://data.ptn.cobrabreiz.services/graphql"):
    try:
        payload = ("{\"query\":\" query {\\n    simulationGet(id: \\\"%s\\\") {\\n        id\\n        status\\n        "
                   "startDate\\n        stopDate\\n        links\\n        error\\n        friendlyName\\n        "
                   "metadata\\n       }\\n}\",\"variables\":{}}") % simulation_id

        response = requests.request("POST", __get_nuant_api_url(api_url), headers=__get_headers(api_key), data=payload)

        result = response.json()

        return result['data']['simulationGet']['links']

    except Exception as e:
        print("An exception occurred: %s" % repr(e))


def fetch_parameters(simulation_id: str, api_key: str ='', api_url: str ="https://data.ptn.cobrabreiz.services/graphql"):
    try:
        list_files = fetch_list_files(simulation_id, api_key, api_url)

        result_link = list_files['parameters.json']

        response_file = requests.request("GET", result_link)

        return response_file.json()
    except Exception as e:
        print("An exception occurred: %s" % repr(e))


def convert_to_singletimeseries(timestamps, values, target='mean', sampling=1):
    from pyquantlib import metrics

    _timestamps = []
    _values = []

    for index, time in enumerate(timestamps['time']):
        current_date = datetime.datetime.fromtimestamp(time, datetime.timezone.utc)

        _timestamps.append(current_date)
        _values.append(values[target][index])

    return metrics.SingleTimeseries.from_components(_timestamps, _values).resample(datetime.timedelta(days=sampling))


def convert_from_singletimeseries(singletimeseries, target='mean'):
    _timestamps = singletimeseries.timestamps()
    _values = singletimeseries.values()

    rows = []
    for index, date in enumerate(_timestamps):
        dict = {}
        dict['date'] = date.isoformat().replace('+00:00', 'Z')
        dict[target] = _values[index]

        rows.append(dict)

    return rows

def fetch_agent_list(simulation_id: str, api_key: str = '', api_url: str = "https://data.ptn.cobrabreiz.services/graphql"):
    parameters = fetch_parameters(simulation_id=simulation_id, api_key=api_key, api_url=api_url)

    agent_list= []

    for agent in parameters['agents']:
        wallet = ', '.join(f'{k}:{v}' for k, v in agent['wallet'].items())
        agent_list.append({'name':agent['name'], 'wallet':wallet})

    return agent_list