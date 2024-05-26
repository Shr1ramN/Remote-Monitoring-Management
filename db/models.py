from datetime import datetime
from pydantic import BaseModel
from datetime import datetime


class device_info(BaseModel):
    _id:str
    device_id: str
    user_id: str
    device_name: str
    description: str
    created_at: datetime
    updated_at: datetime 

# class device_status(BaseModel):
#     device_id: str
#     device_name: str
#     status: str
#     cpu_load: int
#     memory_usage: int
#     time_stamp: str
    
class device_status(BaseModel):
    cpu: dict
    memory: dict
    disk: dict
    network: dict
    mac_address: str
    time_stamp: str
    
class user_info(BaseModel):
    user_id: str
    user_name: str
    password: str
    email:str
    role:str
    
    
class device(BaseModel):
    _id:str
    device_id: str
    user_id: str
    device_name: str
    description: str
    created_at: datetime
    updated_at: datetime 
    status:str