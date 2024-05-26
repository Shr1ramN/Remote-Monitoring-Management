import logging
from core.config import connection_string, user_collection, dbname, device_collection, device_status_collection

import pymongo

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s',
    filename="crud.log" )

#connection establishment of mongo
client = pymongo.MongoClient(connection_string)
logging.info("Connection Established")

db=client[dbname]#connection to database
users_collection= db[user_collection]#connection to users collection
devices_collection  = db[device_collection]#connection to devices collection
status_collection = db[device_status_collection]#connection to status collection


