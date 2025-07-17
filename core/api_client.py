from utils.config_loader import load_config
import requests
import yaml
import os


class APIClient:
    def __init__(self):
        config = load_config()
        self.base_url = config['base_url']
        self.headers = config.get('headers', {})
        self.timeout = config.get('timeout', 0)

    def get(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params, timeout=self.timeout)
        return response

    def post(self, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, headers=self.headers, json=data, timeout=self.timeout)
        return response

    def put(self, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.put(url, headers=self.headers, json=data, timeout=self.timeout)
        return response

    def patch(self, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.patch(url, headers=self.headers, json=data, timeout=self.timeout)
        return response

    def delete(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        response = requests.delete(url, headers=self.headers, timeout=self.timeout)
        return response