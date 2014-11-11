import json
import numpy
import time
from common import nodelist
from server import constants
from server.couchbase import store, util, fetchdocument
from server.couchbase.views import util as view_util
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


def get_view_node_id_attribute_async( node_id, value_type, limit=3000, start_time="", end_time ="{}"):
    log.debug("Get view by node ID for node: %s" %node_id)

    #for given node_id get value_type ordered by time (most recent first)
    db = store.get_bucket()

    if(start_time==""):
        str_startkey = "[\"" + node_id + "\"]"
    else:
        str_startkey = "[\"" + node_id + "\"," + str(start_time)+"]"
    str_endkey = "[\"" + node_id + "\"," + str(end_time)+"]"

    view_by_node_id = db.view('_design/node-timestamp/_view/get_node-timestamp', startkey=str_endkey, endkey = str_startkey,limit=limit, descending = True, include_docs= True)

    all_values = []

    for node in view_by_node_id:
        json = node['doc']
        document = json['json']
        value = float(documentparser.get_value(document, value_type))
        server_timestamp = documentparser.return_server_timestamp(document) * 1000 #convert to milliseconds for javascript
        all_values.insert(1, [server_timestamp,value]) # Keep most recent value at the end of the list to show graph as ascending time line

    return all_values


def get_view_all_nodes_most_recent():
    log.debug("Get most recent view for all nodes")

    db = store.get_bucket()

    all_values = {}

    view_by_node_most_recent = db.view('_design/node-mostrecent/_view/get_node-mostrecent', include_docs= True)

    for node in view_by_node_most_recent:

        json_value = node['doc']
        document = json_value['json']
        name = documentparser.get_value(document, "name")
        nodeid = documentparser.get_value(document, "nodeid")
        disk_size = documentparser.get_value(document, "disk_size")
        load_avg_1min = documentparser.get_value(document, "load_avg_1min")
        memory_percent_used = documentparser.get_value(document, "memory_percent_used")
        uptime_secs = documentparser.get_value(document, "uptime")
        last_updated = documentparser.return_server_time(document)
        total_memory = documentparser.get_value(document,"total_memory")
        num_cpu = documentparser.get_value(document, "number_of_cpus")
        cpu_usage = documentparser.get_value(document, "total_cpu_usage")
        data_sent= documentparser.get_value(document, "network_total_bytes_sent_last_sec")
        data_received = documentparser.get_value(document, "network_total_bytes_received_last_sec")

        ## Human readability######
        uptime = util.convert_secs_to_time_elapsed(uptime_secs)
        disk_size,total_memory,data_sent, data_received = util.convert_bytes_to_human_readable([disk_size,total_memory, data_sent, data_received])


        all_values.update({nodeid:{'num_cpu': num_cpu, 'percent_usage': cpu_usage ,
                       'last_updated': last_updated , 'name':name, 'total_memory': total_memory ,
                       'disk_size':disk_size, 'load_avg_1min':load_avg_1min, 'memory_percent_used':memory_percent_used, 'data_sent':data_sent,
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

        nodeid = documentparser.get_value(document, "nodeid")

        all_synthesized_values.update({nodeid: {'ping_status':ping_status, 'port_status':port_status, 'serial':count}})


    return all_synthesized_values


def get_view_inter_node_trace(node_id):
    document = fetchdocument.fetch_most_recent_document(node_id)
    if(document):
        return document

def get_view_all_nodes_trace():
    log.debug("Get most recent view of trace for all nodes")

    db = store.get_bucket()

    all_trace_values = {}

    view_by_node_trace_most_recent = db.view('_design/node-trace-mostrecent/_view/get_node-trace-mostrecent', include_docs= True)

    ping_status = None
    port_status = None
    count = 0
    for node in view_by_node_trace_most_recent:
        count += 1
        json_value = node['doc']
        document = json_value['json']

        trace =  documentparser.get_value(document, "trace")

        name = documentparser.get_value(document, "nodeid")

        all_trace_values.update({name: {'trace':trace, 'serial':count}})


    return all_trace_values

def get_view_all_nodes_inter_trace():
    log.debug("Get most recent view of inter-trace for all nodes")

    db = store.get_bucket()

    all_trace_values = {}

    view_by_node_trace_most_recent = db.view('_design/node-trace-mostrecent/_view/get_node-trace-mostrecent', include_docs= True)

    ping_status = None
    port_status = None
    count = 0
    for node in view_by_node_trace_most_recent:
        count += 1
        json_value = node['doc']
        document = json_value['json']

        inter_trace =  documentparser.get_value(document, "inter-trace")

        name = documentparser.get_value(document, "nodeid")

        all_trace_values.update({name: {'inter-trace':inter_trace, 'serial':count}})


    return all_trace_values


def get_view_all_nodes_average_attribute_treemap( start_timestamp="", end_timestamp ="{}", group_level=1):


    start_time_key = ""
    end_time_key = ""
    date_attributes = ['year', 'month', 'date', 'hour', 'minute', 'second']
    pattern_list = ['%Y', '%m', '%d', '%H', '%M','%S']

    pattern= "\'"+(', '.join(pattern_list[:group_level-1]))+"\'"


    print "pattern: "+ pattern

    db = store.get_bucket()

    #Treemap--CPU Usage and Free memory
    values_treemap_cpu = [['Id', 'parent', 'metricvalue'], ['Average CPU Usage', '', 0]]
    values_treemap_mem_used = [['Id', 'parent', 'metricvalue'], ['Average Memory Usage', '', 0]]
    values_treemap_data_sent = [['Id', 'parent', 'metricvalue'], ['Average Data Sent', '', 0]]
    values_treemap_data_received = [['Id', 'parent', 'metricvalue'], ['Average Data Received', '', 0]]

    if(start_timestamp==""):
        str_startkey = "[\"""\"]"
    else:
        start_time = util.convert_epoch_to_date_time_dict_attributes_strip_zeroes(start_timestamp)
        for i in range(group_level-1):
            start_time_key += start_time[date_attributes[i]]+","
        start_time_key=start_time_key.rstrip(",")

        str_startkey = "[\"" "\"," + start_time_key+"]"


    if(end_timestamp!= "{}"):
        end_time = util.convert_epoch_to_date_time_dict_attributes_strip_zeroes(end_timestamp)
        for i in range(group_level-1):
            end_time_key += end_time[date_attributes[i]]+","
        end_time_key=end_time_key.rstrip(",")
        str_endkey = "[\"{}\"," + end_time_key+"]"

    else:
        str_endkey = "[\"{}\"," + end_timestamp+"]"

    log.info( "startkey: "+ str_startkey)
    log.info( "endkey: "+ str_endkey)


    view_stats_cpu = db.view('_design/all_nodes_cpu_stats/_view/get_all_nodes_cpu_stats', startkey=str_endkey, endkey = str_startkey, descending = True, reduce=True, group=True, group_level=group_level)


    view_stats_mem = db.view('_design/all_nodes_mem_used/_view/get_all_nodes_mem_used', startkey=str_endkey, endkey = str_startkey, descending = True, reduce=True, group=True, group_level=group_level)


    view_stats_net_sent = db.view('_design/all_nodes_bytes_sent/_view/get_all_nodes_bytes_sent', startkey=str_endkey, endkey = str_startkey, descending = True, reduce=True, group=True, group_level=group_level)


    view_stats_net_received = db.view('_design/all_nodes_bytes_recv/_view/get_all_nodes_bytes_recv', startkey=str_endkey, endkey = str_startkey, descending = True, reduce=True, group=True, group_level=group_level)


    node_id_cpu_avg = view_util.get_sum_count(view_stats_cpu)
    node_id_mem_used_avg = view_util.get_sum_count(view_stats_mem)
    node_id_net_sent_avg = view_util.get_sum_count(view_stats_net_sent)
    node_id_net_received_avg = view_util.get_sum_count(view_stats_net_received)

    for key,value in node_id_cpu_avg.items():
        values_treemap_cpu.append([key, 'Average CPU Usage',value['total_sum']/value['total_count']])

    for key,value in node_id_mem_used_avg.items():
        values_treemap_mem_used.append([key, 'Average Memory Usage',value['total_sum']/value['total_count']])

    for key,value in node_id_net_sent_avg.items():
        values_treemap_data_sent.append([key, 'Average Data Sent', value['total_sum']/value['total_count']])

    for key,value in node_id_net_received_avg.items():
        values_treemap_data_received.append([key, 'Average Data Received', value['total_sum']/value['total_count']])


    return node_treemap(cpu_usage= values_treemap_cpu, memory_usage= values_treemap_mem_used, data_sent= values_treemap_data_sent,
        data_received= values_treemap_data_received)



def get_view_all_nodes_average_attribute_treemap_bkup(limit =10, start_time="", end_time ="{}"):
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

def get_view_nodes_set_metric_stat_aggregated(set, interface, metric, node_id=None, start_timestamp="", end_timestamp ="{}", group_level=1):
    log.debug("Get view by node ID for node: %s" %node_id)

    print "group level: "+ str(group_level)


    start_time_key = ""
    end_time_key = ""
    date_attributes = ['year', 'month', 'date', 'hour', 'minute', 'second']
    pattern_list = ['%Y', '%m', '%d', '%H', '%M','%S']

    pattern= "\'"+(', '.join(pattern_list[:group_level-3]))+"\'"


    print "pattern: "+ pattern

    db = store.get_bucket()

    if(start_timestamp==""):
        str_startkey = "[\"" + node_id + "\","+"\"" +interface+"\""+","+"\""+ metric+"\"" + "]"
    else:
        start_time = util.convert_epoch_to_date_time_dict_attributes_strip_zeroes(start_timestamp)
        for i in range(group_level-3):
            start_time_key += start_time[date_attributes[i]]+","
        start_time_key=start_time_key.rstrip(",")

        str_startkey = "[\"" + node_id + "\"," +"\""+interface+"\""+ "," + "\""+metric +"\""+"," + start_time_key+"]"


    if(end_timestamp!= "{}"):
        end_time = util.convert_epoch_to_date_time_dict_attributes_strip_zeroes(end_timestamp)
        for i in range(group_level-3):
            end_time_key += end_time[date_attributes[i]]+","
        end_time_key=end_time_key.rstrip(",")
        str_endkey = "[\"" + node_id + "\"," +"\""+interface+"\""+","+"\""+ metric+"\""+","+ end_time_key+"]"

    else:
        str_endkey = "[\"" + node_id + "\","+"\""+interface+"\""+","+"\""+ metric+"\"" +","+ end_timestamp+"]"

    log.info( "startkey: "+ str_startkey)
    log.info( "endkey: "+ str_endkey)

    view_stats= []

    if set =='network':
        view_stats = db.view('_design/all_nodes_network_stat/_view/get_all_nodes_network_stat', startkey=str_endkey, endkey = str_startkey, descending = True, reduce=True, group=True, group_level=group_level)

    if set == 'disk':
        view_stats = db.view('_design/all_nodes_disk_stat/_view/get_all_nodes_disk_stat', startkey=str_endkey, endkey = str_startkey, descending = True, reduce=True, group=True, group_level=group_level)

    all_values = []

    for view in view_stats:
        document = view['value']
        avg = document['sum']/document['count']
        key = view['key']
        log.info( 'key: '+str(key) +'avg: '+str(avg))
        date_as_string= "\'"+str(key[3:]).strip('[]')+"\'"

        epoch_milli= util.convert_time_to_epoch(date_as_string,pattern) *1000 #multiply by 1000 to convert to milliseconds
        all_values.insert(1, [epoch_milli,avg])

    return all_values


def get_view_nodes_metric_stat_aggregated(metric, node_id=None, start_timestamp="", end_timestamp ="{}", group_level=1):
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
        start_time = util.convert_epoch_to_date_time_dict_attributes_strip_zeroes(start_timestamp)
        for i in range(group_level-1):
            start_time_key += start_time[date_attributes[i]]+","
        start_time_key=start_time_key.rstrip(",")

        str_startkey = "[\"" + node_id + "\"," + start_time_key+"]"


    if(end_timestamp!= "{}"):
        end_time = util.convert_epoch_to_date_time_dict_attributes_strip_zeroes(end_timestamp)
        for i in range(group_level-1):
            end_time_key += end_time[date_attributes[i]]+","
        end_time_key=end_time_key.rstrip(",")
        str_endkey = "[\"" + node_id + "\"," + end_time_key+"]"

    else:
        str_endkey = "[\"" + node_id + "\"," + end_timestamp+"]"

    log.info( "startkey: "+ str_startkey)
    log.info( "endkey: "+ str_endkey)

    view_stats= []

    if(metric == 'total_cpu_usage'):
        view_stats = db.view('_design/all_nodes_cpu_stats/_view/get_all_nodes_cpu_stats', startkey=str_endkey, endkey = str_startkey, descending = True, reduce=True, group=True, group_level=group_level)

    elif(metric == 'memory_percent_used'):
        view_stats = db.view('_design/all_nodes_mem_used/_view/get_all_nodes_mem_used', startkey=str_endkey, endkey = str_startkey, descending = True, reduce=True, group=True, group_level=group_level)


    elif(metric == 'network_total_bytes_sent_last_sec'):
        view_stats = db.view('_design/all_nodes_bytes_sent/_view/get_all_nodes_bytes_sent', startkey=str_endkey, endkey = str_startkey, descending = True, reduce=True, group=True, group_level=group_level)


    elif(metric == 'network_total_bytes_received_last_sec'):
        view_stats = db.view('_design/all_nodes_bytes_recv/_view/get_all_nodes_bytes_recv', startkey=str_endkey, endkey = str_startkey, descending = True, reduce=True, group=True, group_level=group_level)


    elif(metric == 'load_avg_1min'):
        view_stats = db.view('_design/all_nodes_load_avg/_view/get_all_nodes_load_avg', startkey=str_endkey, endkey = str_startkey, descending = True, reduce=True, group=True, group_level=group_level)


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
