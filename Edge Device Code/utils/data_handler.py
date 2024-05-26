# Data collection, processing, transmission
from datetime import datetime
from getmac import get_mac_address
import psutil


mac = get_mac_address()


for i in range(1):
    system = {}

    # CPU Information
    cpu_info = {}
    cpu_info['cpu_utilization'] = psutil.cpu_percent(interval=1)
    cpu_info['cpu_cores'] = psutil.cpu_count()
    system["cpu"] = cpu_info

    # Memory Information
    mem_info = {}
    mem = psutil.virtual_memory()
    mem_info['total'] = mem.total / (1024 ** 3)  # Convert to GB
    mem_info['available'] = mem.available / (1024 ** 3)  # Convert to GB
    mem_info['percent'] = mem.percent
    system["memory"] = mem_info

    # Disk Information
    disk_info = {}
    disk = psutil.disk_usage('/')
    disk_info['total'] = disk.total / (1024 ** 3)  # Convert to GB
    disk_info['used'] = disk.used / (1024 ** 3)  # Convert to GB
    disk_info['free'] = disk.free / (1024 ** 3)  # Convert to GB
    disk_info['percent'] = disk.percent
    system["disk"] = disk_info

    # Network Information
    net_info = {}
    net = psutil.net_io_counters()
    net_info['bytes_sent'] = net.bytes_sent
    net_info['bytes_recv'] = net.bytes_recv
    system["network"] = net_info

    # Get the current date and time
    current_datetime = datetime.now()

    # Format the datetime object
    formatted_datetime = current_datetime.isoformat()

    system["mac_address"] = get_mac_address()
    system["time_stamp"] = formatted_datetime
    system_info=system