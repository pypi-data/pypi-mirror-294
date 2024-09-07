import os
import socket
import uuid
import requests
import time
from functools import wraps

class OpenFunnelTelemetryBase:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://telemetry.openfunnel.dev/actionTracker"
    
    def get_ip_address(self):
        return requests.get('https://api.ipify.org').text
    
    def get_device_identifier(self):
        return str(uuid.uuid4())
    
    def is_cloud_provider(self):
        cloud_providers = ['amazon', 'google', 'microsoft', 'alibaba', 'oracle']
        hostname = socket.gethostname().lower()
        return any(provider in hostname for provider in cloud_providers)
    
    def send_telemetry(self, data, path):
        telemetry_path = self.api_url + path
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(self.api_url, json=data, headers=headers)
        return response.json()