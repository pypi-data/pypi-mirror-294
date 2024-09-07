import time
from functools import wraps
from openfunnel_telemetry.openfunneltelemetrybase import OpenFunnelTelemetryBase

class OpenFunnelCodeLevelTelemetry(OpenFunnelTelemetryBase):
    def __init__(self, api_key):
        super().__init__(api_key)
    
    def openfunneltelemetry(self):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()
                
                telemetry_data = {
                    "type": "code_level",
                    "function_name": func.__name__,
                    "execution_time": end_time - start_time,
                    "args": args,
                    "kwargs": kwargs,
                    "result": result,
                    "ip_address": self.get_ip_address(),
                    "device_identifier": self.get_device_identifier(),
                    "is_cloud_provider": self.is_cloud_provider()
                }
                
                self.send_telemetry(telemetry_data, "")
                return result
            return wrapper
        return decorator