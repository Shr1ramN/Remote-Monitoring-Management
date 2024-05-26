# General utility functions
import requests

from utils.data_handler import mac,system_info

def get_mac_address1():
    """Retrieves the device's MAC address."""
    return mac


def collect_system_info():
    """Collects and formats system information."""
    return system_info

def send_system_info_and_heartbeat(system_info, heartbeat, backend_url):
    """Sends system information and heartbeat to the backend server."""
    try:
        if system_info:
            # Send system information
            response = requests.post(backend_url + "/receive_data", json=system_info)
            response.raise_for_status()

        if heartbeat:
            # Send heartbeat
            response = requests.post(backend_url + "/heartbeat", json=heartbeat)
            response.raise_for_status()

        print("System information and heartbeat sent successfully!")
    except Exception as e:
        print(f"Error sending information: {e}")

# def send_system_info(system_info, backend_url):
#     try:
#         response = requests.post(backend_url, json=system_info)
#         response.raise_for_status()
#         print("System information sent successfully!")
#     except Exception as e:
#         print(f"Failed to send system information: {e}")