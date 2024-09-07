import time
import platform
from openfunnel_telemetry.openfunneltelemetrybase import OpenFunnelTelemetryBase

class PostInstallHookSDK(OpenFunnelTelemetryBase):
    def __init__(self, api_key):
        super().__init__(api_key)
    
    def post_install_hook(self):
        telemetry_data = {
            "type": "post_install",
            "ip_address": self.get_ip_address(),
            "device_identifier": self.get_device_identifier(),
            "is_cloud_provider": self.is_cloud_provider(),
            "python_version": platform.python_version(),
            "os_info": platform.platform(),
            "install_time": time.time()
        }
        return self.send_telemetry(telemetry_data)

def run_post_install_hook():
    # You might want to get this API key from an environment variable or config file
    post_install_sdk = PostInstallHookSDK("")
    post_install_sdk.post_install_hook()