# client/client.py
import requests
import pandas as pd
from getpass import getpass

class Client:
    def __init__(self, server_url, username=None, password=None):
        self._server_url = server_url
        self._username = username if username is not None else input("Enter your username: ")
        self._password = password if password is not None else getpass(f"Enter {self._username}'s password: ")
        self._token = None
        self._endpoints = self._fetch_endpoints()

    def _authenticate(self):
        auth_endpoint = f"{self._server_url}/auth/token"
        auth_payload = {'username': self._username, 'password': self._password}
        response = requests.post(auth_endpoint, data=auth_payload)
        if response.status_code == 200:
            self._token = response.json()['data'].get('access_token')
        else:
            raise Exception(f"Authentication failed: {response.status_code}, {response.text}")

    def _fetch_endpoints(self):
        openapi_url = f"{self._server_url}/openapi.json"
        response = requests.get(openapi_url)
        if response.status_code == 200:
            openapi_spec = response.json()
            paths = openapi_spec.get('paths', {}).keys()
            if self._username != "admin":
                paths = filter(lambda x: not x.startswith("/admin"), paths)
            return set(paths)
        else:
            raise Exception(f"Failed to fetch OpenAPI spec: {response.status_code}, {response.text}")

    def _get_headers(self):
        if not self._token:
            self._authenticate()
        return {
            'Authorization': f'Bearer {self._token}',
            'Content-Type': 'application/json',
            'X-Username': self._username
        }

    def call_endpoint(self, endpoint='', endpoint_type='post', payload=None):
        if endpoint not in self._endpoints:
            raise ValueError(f"Endpoint '{endpoint}' does not exist.")

        url = f"{self._server_url}/{endpoint.lstrip('/')}"
        headers = self._get_headers()
        response = None

        if endpoint_type.lower() == 'post':
            response = requests.post(url, json=payload, headers=headers)
        elif endpoint_type.lower() == 'get':
            response = requests.get(url, params=payload, headers=headers)
        else:
            raise ValueError("Unsupported endpoint type. Use 'post' or 'get'.")

        if response.status_code == 401:
            self._authenticate()
            headers = self._get_headers()
            if endpoint_type.lower() == 'post':
                response = requests.post(url, json=payload, headers=headers)
            elif endpoint_type.lower() == 'get':
                response = requests.get(url, params=payload, headers=headers)

        return response

    @staticmethod
    def extract_data_from_response(response, as_dataframe=True):
        if response.status_code == 200:
            api_response = response.json()
            if api_response['status'] == 'success':
                data = api_response['data']
                if as_dataframe:
                    if isinstance(data, list) and all(isinstance(i, dict) for i in data):
                        return pd.DataFrame(data)
                    else:
                        raise ValueError("Data is not in the correct format for DataFrame conversion")
                else:
                    return data
            else:
                raise Exception(f"API error: {api_response.get('message', 'Unknown error')}")
        else:
            raise Exception(f"Request failed: {response.status_code}, {response.text}")
