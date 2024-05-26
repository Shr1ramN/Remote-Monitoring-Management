import time
from datetime import datetime
from utils.network_handler import backend_url
from utils.utils import get_mac_address1,collect_system_info,send_system_info_and_heartbeat

if __name__ == "__main__":
    last_data_sent = time.time()
    last_heartbeat_sent = time.time()
    try:
        while True:
            # Get current time
            current_time = time.time()

            if current_time - last_data_sent >= 50:
                system_info = collect_system_info()
                send_system_info_and_heartbeat(system_info, None, backend_url)
                last_data_sent = current_time

            # Send heartbeat every 1 minute
            if current_time - last_heartbeat_sent >= 60:
                heartbeat = {"mac_address": get_mac_address1(), "time_stamp": datetime.now().isoformat()}
                send_system_info_and_heartbeat(None, heartbeat, backend_url)
                last_heartbeat_sent = current_time

            time.sleep(1)  # Sleep for 1 second to avoid high CPU usage
    except KeyboardInterrupt:
        print("Loop stopped by user.")
    
