from datetime import timedelta


connection_string="mongodb+srv://adarsh:admin%40123@cluster0.03woj0o.mongodb.net/"
dbname='remote'
device_collection = 'devices'
user_collection = 'users'
device_status_collection= 'device_status'

# Dictionary to store device last seen timestamps (key: MAC address, value: datetime)
last_seen = {}
# Define timeout threshold (e.g., twice the heartbeat interval)
timeout_threshold = timedelta(minutes=1)  # Adjust based on your heartbeat frequency