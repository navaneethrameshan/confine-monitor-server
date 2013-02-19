import datetime
import time
import calendar
import server.constants
from server.process import fetchdocument, util

def get_value( document, value_type):
    value_type = 'server.constants.' + value_type
    attributes = eval(value_type)
    attribute_list = attributes.split('.')
    value = document
    for attribute in attribute_list:
        value = value[attribute]

    return value

def return_server_timestamp(document):
    server_timestamp_secs = document['server_timestamp']
    #elapsed_time = time.time() - server_timestamp_secs
    #server_timestamp = str(datetime.timedelta(seconds= elapsed_time))
    return server_timestamp_secs

def return_server_time(document):
    server_timestamp = return_server_timestamp(document)
    server_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(server_timestamp))
    print  server_time


if __name__ == '__main__':
    document = fetchdocument.fetch_most_recent_document('Node-1')
    #print document
    return_server_time(document)

