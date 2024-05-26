from datetime import datetime
from uuid import uuid4
from fastapi import HTTPException
from pymongo import ReturnDocument
import pymongo

from db.database import devices_collection, users_collection, status_collection
from db.models import user_info, device_info, device_status
from typing import List

import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s',
    filename="crud.log" )

# Device Functions

def find_device(device_id: str) -> dict:
    """
    Finds a device by its ID in the database.

    Args:
        device_id (str): The ID of the device to find.

    Returns:
        dict: A dictionary containing the device details or raises an HTTPException
               if not found.
    """
    device_details = devices_collection.find_one({"device_id": device_id})
    if not device_details:
        logging.exception(status_code=404, detail="Device not found {device_details}")
        raise HTTPException(status_code=404, detail="Device not found {device_details}")
    logging.info(f"Device found {device_details}")
    return device_details


def find_devices() -> List[device_info]:
    """
    Retrieves all devices from the database.

    Returns:
        List[device_info]: A list of dictionaries containing details of all devices or
                    raises an HTTPException if no devices are found.
    """
    all_devices = list(devices_collection.find())
    if not all_devices:
        logging.exception(status_code=404, detail="No devices")
        raise HTTPException(status_code=404, detail="No devices")

    # Add created_at and updated_at fields to each device dictionary
    for device in all_devices:
        device['created_at'] = datetime.now()
        device['updated_at'] = datetime.now()

    logging.info(f"Displayed all devices: {all_devices}")
    return all_devices


async def insert_device(device: device_info, user_id: str = None):
    """
    Inserts a new device into the database.

    Args:
        device (device_info): A Pydantic model representing the device information.
        user_id (str, optional): The ID of the user who owns the device. Defaults to None.

    Returns:
        dict: A dictionary containing the inserted device data or raises an HTTPException
              if an error occurs.
    """

    try:
        _id = uuid4().hex
        now = datetime.utcnow()
        device_data = {
            "_id":_id,
            "device_id": device.device_id,
            "device_name": device.device_name,
            "description": device.description,
            "created_at": now,
            "updated_at": now,
        }
        if user_id:
            user = users_collection.find_one({"user_id": user_id})
            if user:
                device_data["user_id"] = user_id
            else:
                logging.exception(status_code=404, detail="User not found")
                raise HTTPException(status_code=404, detail="User not found")
        devices_collection.insert_one(device_data)
        logging.info(f"User inserted successfully {device_data}")
        return device_data
    except Exception as e:
        logging.exception(status_code=500, detail=f"Error creating device: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating device: {e}")


async def update_device_info(device_id: str, updated_device: device_info) -> dict:
    """ 
    Updates an existing device in the database.

    Args:
        device_id (str): The ID of the device to update.
        updated_device (device_info): A Pydantic model containing the updated device information.

    Returns:
        dict: A dictionary containing the updated device data or raises an HTTPException
              if not found.
    """
    existing_device = devices_collection.find_one({"device_id": device_id})
    if not existing_device:
        logging.exception(status_code=404, detail="Device not found")
        raise HTTPException(status_code=404, detail="Device not found")
    updated_device_dict = updated_device.dict()
    result = devices_collection.find_one_and_update(
        {"device_id": device_id},
        {"$set": updated_device_dict},
        return_document=ReturnDocument.AFTER
    )
    if not result:
        logging.exception(status_code=404, detail="Device not found")
        raise HTTPException(status_code=404, detail="Device not found")
    result_dict = dict(result)
    result_dict.pop('_id', None)
    logging.info(f"Updated device successfully {result_dict}")
    return result_dict


async def perform_delete_device(device_id: str):
    """
    Deletes a device from the database by its ID.

    Args:
        device_id (str): The ID of the device to delete.

    Returns:
        dict: A dictionary containing a success message or error message.

    Raises:
        HTTPException: If the device with the provided ID cannot be found.
    """
    existing_device = devices_collection.find_one({"device_id": device_id})
    if not existing_device:
        logging.exception(status_code=404, detail="Device not existing")
        raise HTTPException(status_code=404, detail="Device not existing")
    result = devices_collection.delete_one({"device_id": device_id})
    if result.deleted_count == 0:
        logging.exception(status_code=404, detail="Device cannot be deleted ")
        raise HTTPException(status_code=404, detail="Device cannot be deleted")
    logging.info(f"Device deleted successfully with device_id {device_id}")
    return {"message": "Device deleted successfully"}


#user function

def find_user(user_id: str)-> dict:
    """
    Finds a user by their ID in the database.

    Args:
        user_id (str): The ID of the user to find.

    Returns:
        dict: A dictionary containing the user details or raises an HTTPException
               if not found.
    """
    user_details = users_collection.find_one({"user_id": user_id})
    if not user_details:
        logging.exception(status_code=404, detail="No user found")
        raise HTTPException(status_code=404, detail="No user found")
    logging.info("User found successfully ",user_details)
    return user_details

   
def find_users()-> List[dict]:
    """
    Retrieves all users from the database.

    Returns:
        List[dict]: A list of dictionaries containing details of all users or
                    raises an HTTPException if no users are found.
    """
    all_users = list(users_collection.find())
    if not all_users:
        logging.exception(status_code=404, detail="No users found")
        raise HTTPException(status_code=404, detail="No users found")
    logging.info("Users found successfully ",all_users)
    return all_users


def insert_user(user)-> dict:
    """
    Inserts a new user into the database.

    Args:
        user (user_info): A Pydantic model representing the user information.

    Returns:
        dict: A dictionary containing the inserted user data or raises an HTTPException
              if an error occurs.
    """
    result =users_collection.insert_one(dict(user))
    if not result:
        logging.exception(status_code=404, detail="User cannot be inserted")
        raise HTTPException(status_code=404, detail="User cannot be inserted")
    logging.info("User inserted successfully :",user)
    return user


def update_user(user_id: str, updated_fields: dict) -> dict:
    """
    Updates an existing user in the database.

    Args:
        user_id (str): The ID of the user to update.
        updated_fields (dict): A dictionary containing the fields to update.

    Returns:
        dict: A dictionary containing the updated user data or raises an HTTPException
              if not found.
    """
    try:
        now = datetime.utcnow()
        updated_fields["updated_at"] = now
        result = users_collection.update_one({"user_id": user_id}, {"$set": updated_fields})  
        if result.modified_count == 1:
            updated_fields["user_id"] = user_id
            logging.info(f"user updated successfully {updated_fields}")
            return updated_fields
        else:
            logging.exception(status_code=404, detail=f"User with ID {user_id} not found")
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    except Exception as e:
        logging.exception(status_code=500, detail=f"Error updating user: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating user: {e}")
      

def delete_users(user_id:str)-> dict:
    """
    Deletes a user from the database.

    Args:
        user_id (str): The ID of the user to delete.

    Returns:
        dict: A dictionary containing a success message or error message.
    """
    user_details = users_collection.find_one({"user_id":user_id})
    if user_details:
        users_collection.delete_one(user_details)
        logging.info(f"User deleted successfully  {user_details}")
        return {"User deleted successfully "}
    else:
        logging.error("User not exists")
        return {"User not exists"}
    

#device status functions
    
async def store_received_data(device_info: device_status)-> dict:
    """
    Stores device status data received from a device.

    Args:
        device_info (device_status): A Pydantic model representing the device status information.

    Returns:
        dict: A dictionary containing a success message or error message.
    """
    try:
        
        device_data = device_info.dict()

        # Insert the data into MongoDB
        result = status_collection.insert_one(dict(device_data))

        # Check if data was inserted successfully
        if result.inserted_id:
            logging.info("Data stored successfully")
            return {"message": "Data stored successfully"}
        else:
            logging.exception(status_code=500, detail="Failed to store data in database")
            raise HTTPException(status_code=500, detail="Failed to store data in database")
    except Exception as e:
        # Handle exceptions
        logging.exception(status_code=500, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))
        


def receive_heartbeat(heartbeat, last_seen):
    """
    Processes a heartbeat received from a device.

    Args:
        heartbeat (device_status): A Pydantic model representing the device's status information.
        last_seen (dict): A dictionary containing timestamps for devices.

    Updates the `last_seen` timestamp for the device in the dictionary.

    Raises:
        HTTPException: If the device ID cannot be found in `last_seen`.
    """
    try:
        mac_address = heartbeat["mac_address"]
    except KeyError:
        raise HTTPException(status_code=400, detail="Missing 'mac_address' in heartbeat data")

    last_seen[mac_address] = datetime.now()

    return {"message": "Heartbeat received successfully"}

def get_device_status(last_seen, mac_address, timeout_threshold):
    """
    Determines the online status of a device based on the last seen timestamp.

    Args:
        last_seen (dict): A dictionary containing timestamps for devices.
        mac_address (str): The MAC address of the device to check.
        timeout_threshold (datetime.timedelta): The threshold to determine if a device is offline.

    Returns:
        dict: A dictionary containing the device status ("online" or "offline").
    """
    if mac_address not in last_seen:
        raise HTTPException(status_code=404, detail="Device not found")

    if datetime.now() - last_seen[mac_address] > timeout_threshold:
        return {"status": "offline"}
    else:
        return {"status": "active"}
    
def get_device_stats(mac_address: str ):
    """Retrieves the most recent device status data for a given MAC address."""

    # Find devices with matching MAC address
    device_data = status_collection.find_one({"mac_address": mac_address}, sort=[("time_stamp", pymongo.DESCENDING)])

    if not device_data:
        return {"message": f"Device with MAC address '{mac_address}' not found."}, 404

    # Convert MongoDB document to device_status model
    return device_status(**device_data)  # Unpack document fields into model

def get_device_status2(last_seen, mac_address, timeout_threshold):
    """
    Determines the online status of a device based on the last seen timestamp.

    Args:
        last_seen (dict): A dictionary containing timestamps for devices.
        mac_address (str): The MAC address of the device to check.
        timeout_threshold (datetime.timedelta): The threshold to determine if a device is offline.

    Returns:
        dict: A dictionary containing the device status ("online" or "offline").
    """
    # Check if the device has been seen recently
    if mac_address in last_seen:
        last_seen_time = last_seen[mac_address]
        if datetime.now() - last_seen_time <= timeout_threshold:
            return {"status": "active"}

    # If not seen or seen more than the timeout threshold, consider the device offline
    return {"status": "offline"}
