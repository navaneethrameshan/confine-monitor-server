import json
#import numpy
import time
from common import nodelist
from server import constants
from server.couchbase import store, util, fetchdocument
from server.couchbase import documentparser
from server.logger import logger
from collections import namedtuple

log = logger("Get View")

node_treemap = namedtuple("node_treemap", 'cpu_usage memory_usage data_sent data_received')


def get_view_node_id_attribute_json( node_id, value_type, limit):
    #for given node_id get value_type ordered by time (most recent first)
    log.debug("Get view by node ID for node: %s" %node_id)
    db = store.get_bucket()

    str_startkey = "[\"" + node_id + "\",{}]"
    str_endkey = "[\"" + node_id + "\"]"

    view_by_node_id = db.view('_design/node-timestamp/_view/get_node-timestamp', startkey=str_startkey, endkey = str_endkey, descending = True, include_docs= True, limit=limit)


    all_values = []


    for node in view_by_node_id:
        json = node['doc']
        document = json['json']
        value = documentparser.get_value(document, value_type)
        server_timestamp = documentparser.return_server_timestamp(document) * 1000
        all_values.insert(1, [server_timestamp,value]) # Keep most recent value at the end of the list to show graph as ascending time line

    return all_values


def get_view_node_id_attribute_timeline( node_id, value_type, limit=1000, start_time="", end_time ="{}"):
    log.debug("Get view by node ID for node: %s" %node_id)

    #for given node_id get value_type ordered by time (most recent first)
    db = store.get_bucket()

    if(start_time==""):
        str_startkey = "[\"" + node_id + "\"]"
    else:
        str_startkey = "[\"" + node_id + "\"," + start_time+"]"
    str_endkey = "[\"" + node_id + "\"," + end_time+"]"

    view_by_node_id = db.view('_design/node-timestamp/_view/get_node-timestamp', startkey=str_endkey, endkey = str_startkey,limit=limit, descending = True, include_docs= True)

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

def get_view_all_nodes_most_recent():
    log.debug("Get most recent view for all nodes")

    db = store.get_bucket()

    all_values = {}

    view_by_node_most_recent = db.view('_design/node-mostrecent/_view/get_node-mostrecent', include_docs= True)

    for node in view_by_node_most_recent:

        json_value = node['doc']
        document = json_value['json']

        name = documentparser.get_value(document, "nodeid")
        disk_size = documentparser.get_value(document, "disk_size")
        load_avg_1min = documentparser.get_value(document, "load_avg_1min")
        free_mem = documentparser.get_value(document, "free_memory")
        uptime_secs = documentparser.get_value(document, "uptime")
        last_updated = documentparser.return_server_time(document)
        total_memory = documentparser.get_value(document,"total_memory")
        num_cpu = documentparser.get_value(document, "number_of_cpus")
        cpu_usage = documentparser.get_value(document, "total_cpu_usage")
        data_sent= documentparser.get_value(document, "network_total_bytes_sent_last_sec")
        data_received = documentparser.get_value(document, "network_total_bytes_received_last_sec")

        ## Human readability######
        uptime = util.convert_secs_to_time_elapsed(uptime_secs)
        disk_size,total_memory,free_mem,data_sent, data_received = util.convert_bytes_to_human_readable([disk_size,total_memory,free_mem, data_sent, data_received])


        all_values.update({name:{'num_cpu': num_cpu, 'percent_usage': cpu_usage ,
                       'last_updated': last_updated , 'name':name, 'total_memory': total_memory ,
                       'disk_size':disk_size, 'load_avg_1min':load_avg_1min, 'free_mem':free_mem, 'data_sent':data_sent,
                       'data_received':data_received, 'uptime':uptime}})




    return all_values


def get_view_all_nodes_synthesized_most_recent():
    log.debug("Get most recent synthesized view for all nodes")

    db = store.get_bucket()

    all_synthesized_values = {}

    view_by_node_synthesized_most_recent = db.view('_design/node-synthesized-mostrecent/_view/get_node-synthesized-mostrecent', include_docs= True)

    ping_status = None
    port_status = None
    count = 0
    for node in view_by_node_synthesized_most_recent:
        count += 1
        json_value = node['doc']
        document = json_value['json']

        ping_status =  documentparser.get_value(document, "ping_status")
        port_status = documentparser.get_value(document, "port_status")

        name = documentparser.get_value(document, "nodeid")

        all_synthesized_values.update({name: {'ping_status':ping_status, 'port_status':port_status, 'serial':count}})


    return all_synthesized_values


def get_view_all_nodes_average_attribute_treemap(limit =10, start_time="", end_time ="{}"):
    log.debug("Get view for most recent attribute for all nodes")

    #for given node_id get value_type ordered by time (most recent first)
    db = store.get_bucket()
    count = 0


    #Treemap--CPU Usage and Free memory
    values_treemap_cpu = [['Id', 'parent', 'metricvalue'], ['Average CPU Usage', '', 0]]
    values_treemap_mem_used = [['Id', 'parent', 'metricvalue'], ['Average Memory Usage', '', 0]]
    values_treemap_data_sent = [['Id', 'parent', 'metricvalue'], ['Average Data Sent', '', 0]]
    values_treemap_data_received = [['Id', 'parent', 'metricvalue'], ['Average Data Received', '', 0]]


    for node_id in constants.nodes:
        count+=1
        name = node_id

        load_avg_1min = []
        mem_usage = []
        cpu_usage = []
        data_sent= []
        data_received = []

        if(start_time==""):
            str_startkey = "[\"" + node_id + "\"]"
        else:
            str_startkey = "[\"" + node_id + "\"," + start_time+"]"
        str_endkey = "[\"" + node_id + "\"," + end_time+"]"

        view_by_node_id = db.view('_design/node-timestamp/_view/get_node-timestamp', startkey=str_endkey, endkey = str_startkey,limit=limit, descending = True, include_docs= True)

        count = 0
        for node in view_by_node_id:
            json_value = node['doc']
            document = json_value['json']

            if document:
                load_avg_1min.append(documentparser.get_value(document, "load_avg_1min"))
                mem_usage.append(documentparser.get_value(document, "memory_percent_used"))
                cpu_usage.append(documentparser.get_value(document, "total_cpu_usage"))
                data_sent.append(documentparser.get_value(document, "network_total_bytes_sent_last_sec"))
                data_received.append(documentparser.get_value(document, "network_total_bytes_received_last_sec"))


        #Update Treemap--CPU Usage and Free memory
        values_treemap_cpu.append([name, 'Average CPU Usage', numpy.average(cpu_usage)])
        values_treemap_mem_used.append([name, 'Average Memory Usage', numpy.average(mem_usage)])
        values_treemap_data_sent.append([name, 'Average Data Sent', numpy.average(data_sent)])
        values_treemap_data_received.append([name, 'Average Data Received', numpy.average(data_received)])



    return node_treemap(cpu_usage= values_treemap_cpu, memory_usage= values_treemap_mem_used, data_sent= values_treemap_data_sent,
                        data_received= values_treemap_data_received)



def get_view_nodes_cpu_stat(node_id=None, start_timestamp="", end_timestamp ="{}", group_level=1):
    log.debug("Get view by node ID for node: %s" %node_id)


    start_time_key = ""
    end_time_key = ""
    date_attributes = ['year', 'month', 'date', 'hour', 'minute', 'second']
    pattern_list = ['%Y', '%m', '%d', '%H', '%M','%S']

    pattern= "\'"+(', '.join(pattern_list[:group_level-1]))+"\'"


    print "pattern: "+ pattern

    db = store.get_bucket()

    if(start_timestamp==""):
        str_startkey = "[\"" + node_id + "\"]"
    else:
        start_time = util.convert_epoch_to_date_time_dict_attributes_lstrip(start_timestamp)
        for i in range(group_level-1):
            start_time_key += start_time[date_attributes[i]]+","
        start_time_key=start_time_key.rstrip(",")

        str_startkey = "[\"" + node_id + "\"," + start_time_key+"]"


    if(end_timestamp!= "{}"):
        end_time = util.convert_epoch_to_date_time_dict_attributes_lstrip(end_timestamp)
        for i in range(group_level-1):
            end_time_key += end_time[date_attributes[i]]+","
        end_time_key=end_time_key.rstrip(",")
        str_endkey = "[\"" + node_id + "\"," + end_time_key+"]"

    else:
        str_endkey = "[\"" + node_id + "\"," + end_timestamp+"]"

    log.info( "startkey: "+ str_startkey)
    log.info( "endkey: "+ str_endkey)

    view_stats = db.view('_design/all_nodes_cpu_stats/_view/get_all_nodes_cpu_stats', startkey=str_endkey, endkey = str_startkey, descending = True, reduce=True, group=True, group_level=group_level)

    all_values = []

    for view in view_stats:
        document = view['value']
        avg = document['sum']/document['count']
        key = view['key']
        log.info( 'key: '+str(key) +'avg: '+str(avg))
        date_as_string= "\'"+str(key[1:]).strip('[]')+"\'"

        epoch_milli= util.convert_time_to_epoch(date_as_string,pattern) *1000 #multiply by 1000 to convert to milliseconds
        all_values.insert(1, [epoch_milli,avg])

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
    Document returned from view sliver-timestamp/get_slice-timestamp
    key = [sliver_id, server_timestamp],  value= {'sliver': sliverinfo,'nodeid':nodeid,'server_timestamp': server_timestamp}

    returns
    '''

    log.debug("Get most recent sliver attributes for slice: %s" %slice_id)
    all_values = [['Id', 'parent', 'metricvalue'], [value_type, '', 0]]

    db = store.get_bucket()

    view_by_slice_id =[]

    #nodes = nodelist.get_node_list()
    nodes = constants.nodes

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

   # nodes = nodelist.get_node_list()
    nodes = constants.nodes

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
        server_timestamp = documentparser.get_value(document, "server_timestamp")
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
