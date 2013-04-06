import json
import time
from common import nodelist
from server import constants
from server.couchbase import store, util, fetchdocument
from server.couchbase import documentparser
from server.logger import logger

log = logger("Get View")


def get_view_node_id_attribute( node_id, value_type):
    #for given node_id get value_type ordered by time (most recent first)
    log.debug("Get view by node ID for node: %s" %node_id)
    db = store.get_bucket()

    str_startkey = "[\"" + node_id + "\",{}]"
    str_endkey = "[\"" + node_id + "\"]"

    view_by_node_id = db.view('_design/node-timestamp/_view/get_node-timestamp', startkey=str_startkey, endkey = str_endkey, limit=1000, descending = True, include_docs= True)


    all_values = [['Time', str(value_type)]]


    for node in view_by_node_id:
        json = node['doc']
        document = json['json']
        value = documentparser.get_value(document, value_type)
        server_time = documentparser.return_server_time(document)
        all_values.insert(1,[server_time,value]) # Keep most recent value at the end of the list to show graph as ascending time line

    return all_values


def get_view_node_id_attribute_timeline( node_id, value_type):
    log.debug("Get view by node ID for node: %s" %node_id)

    #for given node_id get value_type ordered by time (most recent first)
    db = store.get_bucket()

    str_startkey = "[\"" + node_id + "\",{}]"
    str_endkey = "[\"" + node_id + "\"]"

    view_by_node_id = db.view('_design/node-timestamp/_view/get_node-timestamp', startkey=str_startkey, endkey = str_endkey,limit=1000, descending = True, include_docs= True)

    all_values = []

    for node in view_by_node_id:
        json = node['doc']
        document = json['json']
        value = documentparser.get_value(document, value_type)
        server_timestamp = documentparser.return_server_timestamp(document)
        date_time_value= util.convert_epoch_to_date_time_javascript(server_timestamp)
        date_time_value.update({'value': value})
        all_values.insert(1, date_time_value) # Keep most recent value at the end of the list to show graph as ascending time line

    return all_values




def get_view_slice_id_attribute_timeline( slice_id, value_type):

    log.debug("Get view by slice ID for slice: %s" %slice_id)

    #for given slice_id get value_type ordered by time (most recent first)
    db = store.get_bucket()
    str_startkey = "[\"" + slice_id + "\",{}]"
    str_endkey = "[\"" + slice_id + "\"]"

    view_by_slice_id = db.view('_design/slice-timestamp/_view/get_slice-timestamp', startkey=str_startkey, endkey = str_endkey, descending = True, limit=1000)

    all_values = []

    for slice in view_by_slice_id:
        document = slice['value']
        value = documentparser.get_value(document, value_type)
        server_timestamp = documentparser.return_server_timestamp(document)
        date_time_value= util.convert_epoch_to_date_time_javascript(server_timestamp)
        sliver_id = documentparser.get_value(document, 'sliver_name')
        date_time_value.update({'value': value, 'sliver_id': sliver_id })
        all_values.insert(1, date_time_value) # Keep most recent value at the end of the list to show graph as ascending time line

    return all_values


def get_view_sliver_id_attribute_timeline( sliver_id, value_type):
    '''
    Document returned from view sliver-timestamp/get_sliver-timestamp
    key = [sliver_id, server_timestamp],  value= {'sliver': sliverinfo,'nodeid':nodeid,'server_timestamp': server_timestamp}

    returns
    '''


    log.debug("Get view by sliver ID for sliver: %s" %sliver_id)

    db = store.get_bucket()

    str_startkey = "[\"" + sliver_id + "\",{}]"
    str_endkey = "[\"" + sliver_id + "\"]"

    view_by_sliver_id = db.view('_design/sliver-timestamp/_view/get_sliver-timestamp', startkey=str_startkey, endkey = str_endkey, descending = True, limit=1000)

    all_values = []

    for row in view_by_sliver_id:
        document = row['value']
        sliver = document['sliver']
        value = documentparser.get_value(sliver, value_type)
        server_timestamp = documentparser.return_server_timestamp(document)
        date_time_value= util.convert_epoch_to_date_time_javascript(server_timestamp)
        date_time_value.update({'value': value})
        all_values.insert(1, date_time_value) # Keep most recent value at the end of the list to show graph as ascending time line

    return all_values


def get_view_sliver_most_recent_attribute_treemap( node_id, value_type):
    '''
    Document returned from view sliver-timestamp/get_sliver-timestamp
    key = [sliver_id, server_timestamp],  value= {'sliver': sliverinfo,'nodeid':nodeid,'server_timestamp': server_timestamp}

    returns
    '''

    log.debug("Get most recent sliver attributes for Node: %s" %node_id)
    all_values = [['Id', 'parent', 'metricvalue'], [value_type, '', 0]]

    document = fetchdocument.fetch_most_recent_document(node_id)
    
    if(document):

        slivers = document['slivers']

        for container in slivers:
            sliver = slivers[container]
            sliver_id = documentparser.get_value(sliver, 'sliver_name')
            value = documentparser.get_value(sliver, value_type)
            all_values.append([sliver_id, value_type, value])

    return all_values


def get_view_slice_most_recent_attribute_treemap( slice_id, value_type):
    '''
    Document returned from view sliver-timestamp/get_sliver-timestamp
    key = [sliver_id, server_timestamp],  value= {'sliver': sliverinfo,'nodeid':nodeid,'server_timestamp': server_timestamp}

    returns
    '''

    log.debug("Get most recent sliver attributes for slice: %s" %slice_id)
    all_values = [['Id', 'parent', 'metricvalue'], [value_type, '', 0]]

    db = store.get_bucket()

    view_by_slice_id =[]

    nodes = nodelist.get_node_list()

    for node in nodes:

        str_startkey = "[\"" + slice_id +"\",\""+ node+ "\",{}]"
        str_endkey = "[\"" + slice_id + "\",\""+ node+ "\"]"

        most_recent_slice = db.view('_design/slice-timestamp/_view/get_slice-timestamp', startkey=str_startkey, endkey = str_endkey, descending = True, limit=1)

        if(len(most_recent_slice)>0):
            view_by_slice_id.append(most_recent_slice[0])


    for slice in view_by_slice_id:
        sliver = slice['value']
        sliver_id = documentparser.get_value(sliver, 'sliver_name')
        value = documentparser.get_value(sliver, value_type)
        all_values.append([sliver_id, value_type, value])

    return all_values


def get_view_slice_id_all_slivers_most_recent( slice_id):
    '''
    Returns a list of the most recent values of all sliver information of a particular slice
    EX: [{sliverid:1,... }, {sliverid:2,... }, ...{sliverid:n, ...}]
    '''

    log.debug("Get all slivers for slice: %s" %slice_id)
    db = store.get_bucket()

    view_by_slice_id =[]

    nodes = nodelist.get_node_list()

    for node in nodes:

        str_startkey = "[\"" + slice_id +"\",\""+ node+ "\",{}]"
        str_endkey = "[\"" + slice_id + "\",\""+ node+ "\"]"

        most_recent_slice = db.view('_design/slice-timestamp/_view/get_slice-timestamp', startkey=str_startkey, endkey = str_endkey, descending = True, limit=1)

        if(len(most_recent_slice)>0):
            view_by_slice_id.append(most_recent_slice[0])

    all_values = []

    for slice in view_by_slice_id:
        document = slice['value']
        all_values.append(document)

    return all_values


def get_view_node_id_synthesized_attribute_timeline( node_id, value_type):
    log.debug("Get view by node ID for node: %s" %node_id)

    #for given node_id get value_type ordered by time (most recent first)
    db = store.get_bucket()

    str_startkey = "[\"" + node_id + "\",{}]"
    str_endkey = "[\"" + node_id + "\"]"

    view_by_node_id = db.view('_design/synthesized-timestamp/_view/get_synthesized-timestamp', startkey=str_startkey, endkey = str_endkey, descending = True, limit=1000, include_docs= True)

    all_values = []

    for node in view_by_node_id:
        json = node['doc']
        document = json['json']
        value = documentparser.get_value(document, value_type)
        server_timestamp = documentparser.get_value(document, "timestamp")
        date_time_value= util.convert_epoch_to_date_time_dict(server_timestamp)
        date_time_value.update({'value': value})
        all_values.append(date_time_value)

    return all_values

def get_view_node_id_synthesized_attribute_most_recent( node_id, value_type):
    log.debug("Get view by node ID for node: %s" %node_id)

    #for given node_id get value_type ordered by time (most recent first)
    db = store.get_bucket()

    str_startkey = "[\"" + node_id + "\",{}]"
    str_endkey = "[\"" + node_id + "\"]"

    view_by_node_id = db.view('_design/synthesized-timestamp/_view/get_synthesized-timestamp', startkey=str_startkey, endkey = str_endkey, descending = True, limit=1, include_docs= True)

    all_values = []

    if(len(view_by_node_id)>0):
        node = view_by_node_id[0]
        json = node['doc']
        document = json['json']
        value = documentparser.get_value(document, value_type)
        return value
