from fastapi import APIRouter
from db.models import user_info, device_info, device_status, device
from crud.crud_item import (
    find_device,
    find_devices,
    insert_device,
    update_device_info,
    perform_delete_device,
    find_user,
    find_users,
    insert_user,
    update_user,
    delete_users,
    store_received_data,
    receive_heartbeat,
    get_device_status,
    get_device_status2,
    get_device_stats,
)
from typing import List
from core.config import last_seen, timeout_threshold

info = APIRouter()


@info.get("/devices", response_model=List[device_info], tags=["DEVICE"])
async def find_all_devices():
    """
    Retrieves a list of all devices from the database.

    Returns:
        List[device_info]: A list containing details of all devices.
    """
    return find_devices()
 
@info.get("/devices/",response_model=device_info,tags=['DEVICE'])
async def find_device_by_id(device_id:str):
    """
    Finds a device by its ID in the database.

    Args:
        device_id (str): The ID of the device to find.

    Returns:
        device_info: A dictionary containing the device details or raises an HTTPException
                    if the device is not found.

    Raises:
        HTTPException: If the device with the provided ID cannot be found.
    """
    return find_device(device_id)


@info.post("/devices", response_model=device_info, tags=["DEVICE"])
async def create_device(device: device_info, user_id: str = None):
    """
    Creates a new device in the database.

    Args:
        device (device_info): A Pydantic model representing the device information.
        user_id (str, optional): The ID of the user who owns the device. Defaults to None.

    Returns:
        device_info: A dictionary containing the inserted device data or raises an HTTPException
                    if an error occurs.
    """
    return await insert_device(device, user_id)


@info.put("/devices/", response_model=dict, tags=["DEVICE"])
async def update_device(device_id: str, request: device_info):
    """
    Updates an existing device in the database.

    Args:
        device_id (str): The ID of the device to update.
        request (device_info): A Pydantic model containing the updated device information.

    Returns:
        dict: A dictionary containing a success message or error message.
    """
    return await update_device_info(device_id, request)


@info.delete("/devices/", response_model=dict, tags=["DEVICE"])
async def delete_device(device_id: str):
    """
    Deletes a device from the database by its ID.

    Args:
        device_id (str): The ID of the device to delete.

    Returns:
        dict: A dictionary containing a success message or error message.
    """
    return await perform_delete_device(device_id)


@info.get("/users", response_model=List[user_info], tags=["USER"])
async def get_all_users():
    """
    Retrieves a list of all users from the database.

    Returns:
        List[user_info]: A list containing details of all users.
    """
    
    return find_users()


# @info.post("/login


@info.get("/users/{user_id}", response_model=user_info, tags=["USER"])
async def get_user(user_id: str) -> user_info:
    """
    Finds a user by their ID in the database.

    Args:
        user_id (str): The ID of the user to find.

    Returns:
        user_info: A dictionary containing the user details or raises an HTTPException
                    if the user is not found.

    Raises:
        HTTPException: If the user with the provided ID cannot be found.
    """
    return find_user(user_id)


@info.post("/users", tags=["USER"])
async def create_user(user: user_info):
    """
    Creates a new user in the database.

    Args:
        user (user_info): A Pydantic model representing the user information.

    Returns:
        user_info: A dictionary containing the inserted user data or raises an HTTPException
                    if an error occurs.
    """

    return insert_user(user)


@info.put("/users/", response_model=dict, tags=["USER"])
async def update_user_by_id(user_id: str, updated_fields: dict[str, str]):
    """
    Updates an existing user in the database.

    Args:
        user_id (str): The ID of the user to update.
        updated_fields (dict[str, str]): A dictionary containing the fields to update and their new values.

    Returns:
        dict: A dictionary containing a success message or error message.
    """
    return update_user(user_id, updated_fields)


@info.delete("/users/{user_id}", tags=["USER"])
async def delete_user(user_id: str):
    """
    Deletes a user from the database by their ID.

    Args:
        user_id (str): The ID of the user to delete.

    Returns:
        dict: A dictionary containing a success message or error message.
    """
    return delete_users(user_id)


@info.post("/receive_data")
async def receive_data(device_info: device_status):
    """
    Stores device status data received from a device.

    Args:
        device_info (device_status): A Pydantic model representing the device status information.

    Returns:
        dict: A dictionary containing a success message or error message.
    """
    return await store_received_data(device_info)


@info.post("/heartbeat")
async def receive_heartbeats(heartbeat: dict):
    """
    Receives heartbeat data from devices and updates the last seen timestamp.

    Args:
        heartbeat (dict): A dictionary containing heartbeat data (format depends on implementation).

    Raises:
        HTTPException: If the device ID cannot be found in `last_seen`.
    """
    return receive_heartbeat(heartbeat, last_seen)


@info.get("/device-status/")
async def get_device_statuss(mac_address: str):
    """
    Returns the online status of a device based on the last received heartbeat.

    Args:
        mac_address (str): The MAC address of the device to check.

    Returns:
        dict: A dictionary containing the device status ("online" or "offline").
    """
    return get_device_status2(last_seen, mac_address, timeout_threshold)

@info.get("/get_device_stats/")
async def get_stats(mac_address:str):
    return get_device_stats(mac_address)


# added api
@info.get("/active-device-status")
async def all_device_status():
    """
    Returns the status of all available devices.

    Returns:
        dict: A dictionary containing MAC addresses as keys and their statuses ("online" or "offline") as values.
    """
    device_statuses = {}
    for mac_address in last_seen:
        status = get_device_status(last_seen, mac_address, timeout_threshold)
        device_statuses[mac_address] = status
    return device_statuses

@info.get("/devices_with_status", response_model=List[device], tags=["Devices"])
async def get_all_devices_with_status():
    """
    Retrieves a list of all devices from the database along with their online/offline status.

    Returns:
        List[device_info]: A list containing details of all devices including their status.
    """
    devices = find_devices()  # Retrieve all devices
    for device in devices:
        device_id = device.get("device_id")  # Access device_id from the dictionary
        status = get_device_status2(last_seen,device_id,timeout_threshold)  # Get status for the device_id
        device["status"] = status["status"]  # Add status to the device dictionary
    return devices

