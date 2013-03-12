import datetime
import time
import calendar
import server.constants
from server.couchbase import fetchdocument, util
from server.logger import logger

log = logger("Document Parser")

def get_value( document, value_type):
    log.debug("Attempting to get value from document %s for value %s" %(document,value_type))
    value_type = 'server.constants.' + value_type
    attributes = eval(value_type)
    log.debug("Path for value is %s" %attributes)
    attribute_list = attributes.split('.')
    value = document
    for attribute in attribute_list:
        value = value[attribute]
    log.debug("Value obtained is: " + str(value))
    return value

def return_server_timestamp(document):
    log.debug("Attempting to get server_timestamp from document %s " %(document))
    server_timestamp_secs = document['server_timestamp']
    log.debug("Server Timestamp is: " + str(server_timestamp_secs))
    return server_timestamp_secs

def return_server_time(document):
    log.debug("Attempting to get server_timestamp as (Year,Month,Day: Hour,Mintues,Seconds) from document %s " %(document))
    server_timestamp = return_server_timestamp(document)
    server_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(server_timestamp))
    log.debug("Server time obtained is " + str(server_time))
    return server_time

def get_set(document, set_type):
    log.debug("Attempting to get value from document %s for value %s" %(document,set_type))
    return document[set_type]

if __name__ == '__main__':
    document = fetchdocument.fetch_most_recent_document('Node-1')
    #print document
    return_server_time(document)

