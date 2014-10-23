import datetime
import time
import calendar
import server.constants
from server.couchbase import fetchdocument, util
from server.logger import logger

log = logger("Document Parser")

def get_value( document, value_type):
    '''
    Get value from variable name in server.constants if it exists, otherwise
    Get value directly from attributes. Used for attributes with dynamic names. Example: value of bytesent for a particular interface
    '''
    value = None

    if(len(document)>0):

        log.debug("Attempting to get value from document %s for value %s" %(document,value_type))
        try:
            new_value_type = 'server.constants.' + value_type
            attributes = eval(new_value_type)
            log.debug("Path for value is %s" %attributes)
        except:
            log.debug("Exception in attempting to evaluate value of " + value_type)
            log.debug("Reset given value to attributes")
            attributes = value_type

        attribute_list = attributes.split('.')
        value = document
        for attribute in attribute_list:
            if attribute in value:
                value = value[attribute]
            else:
                value = None
		break
        if isinstance( value, basestring ): # True for both Unicode and byte strings
            log.debug("Value obtained is: " + value.encode('utf8'))
            value = value.encode('utf8')

    return value


def return_server_timestamp(document):

    if len(document)>0:
        log.debug("Attempting to get server_timestamp from document %s " %(document))
        server_timestamp_secs = document['server_timestamp']
        log.debug("Server Timestamp is: " + str(server_timestamp_secs))
        return server_timestamp_secs

def return_server_time(document):

    if len(document)>0:
        log.debug("Attempting to get server_timestamp as (Year,Month,Day: Hour,Mintues,Seconds) from document %s " %(document))
        server_timestamp = return_server_timestamp(document)
        server_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(server_timestamp))
        log.debug("Server time obtained is " + str(server_time))
        return server_time

def get_set(document, set_type):
    log.debug("Attempting to get set from document %s for value %s" %(document,set_type))
    if(document):
        set = document[set_type]
    else:
        set = None
    return set



