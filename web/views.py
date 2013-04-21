import ast
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context, RequestContext, Template
from django.http import HttpResponse, Http404
import json
import string
from common import nodelist
from server.couchbase import fetchdocument, util, documentparser, store
from server.couchbase.views import getview
from server import constants
import web.metricvalue

def index(request):

    server_ip = util.SERVER_IP
    server_port = util.SERVER_PORT

    all_values = []
    count = 0

    # the initial page to display
    #nodes = nodelist.get_node_list()
    nodes = constants.nodes

    #Treemap--CPU Usage and Free memory
    values_treemap_cpu = [['Id', 'parent', 'metricvalue'], ['Most Recent CPU Usage', '', 0]]
    values_treemap_free_mem = [['Id', 'parent', 'metricvalue'], ['Free Memory', '', 0]]


    for node in nodes:
        count+=1

        document = fetchdocument.fetch_most_recent_document(node)
        name = node

        disk_size = None
        load_avg_1min = None
        free_mem = None
        uptime_secs = None
        last_updated = None
        total_memory = None
        num_cpu = None
        cpu_usage = None
        data_sent= None
        data_received = None
        uptime = None

        if document:
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

            #Update Treemap--CPU Usage and Free memory
            values_treemap_cpu.append([name, 'Most Recent CPU Usage', cpu_usage])
            values_treemap_free_mem.append([name, 'Free Memory', free_mem])



        ## Human readability######
            uptime = util.convert_secs_to_time_elapsed(uptime_secs)
            disk_size,total_memory,free_mem,data_sent, data_received = util.convert_bytes_to_human_readable([disk_size,total_memory,free_mem, data_sent, data_received])

        ping_status = getview.get_view_node_id_synthesized_attribute_most_recent(node,"ping_status")
        port_status = getview.get_view_node_id_synthesized_attribute_most_recent(node,"port_status")




        all_values.append({'num_cpu': num_cpu, 'percent_usage': cpu_usage ,
                           'last_updated': last_updated ,'serial':count, 'name':name, 'total_memory': total_memory ,
                           'disk_size':disk_size, 'load_avg_1min':load_avg_1min, 'free_mem':free_mem, 'data_sent':data_sent,
                           'data_received':data_received, 'uptime':uptime, 'ping_status':ping_status, 'port_status':port_status})




    #Send as JSON objects
    values_treemap_cpu= json.dumps(values_treemap_cpu)
    values_treemap_free_mem =json.dumps(values_treemap_free_mem)


   # Use to strip double quotes and single quotes to pass data for annotated timeline
   # str_values = str(values)
   # modified_string = str_values.replace('\"', ' ').strip().replace("\'", ' ').strip()



    return render_to_response('indexgc.html',{'all_values':all_values, 'values_treemap_cpu':values_treemap_cpu,
                                              'values_treemap_free_mem':values_treemap_free_mem, 'server_ip': server_ip, 'server_port': server_port },
						context_instance=RequestContext(request))


def highstock_node_attribute(request):
    return render_to_response('highstock.html')


def json_node_attribute(request, parameter):
    print "parameter: "+parameter
    group_level=1

    if(parameter):
        str_start_timestamp, str_end_timestamp = parameter.split("&")
        start_timestamp = int(str_start_timestamp.split("=")[-1])/1000  #time is received from javascript in milliseconds
        end_timestamp = int(str_end_timestamp.split("=")[-1])/1000 #change milliseconds to seconds
        range = end_timestamp- start_timestamp

        global group_level

        # find the right range
        # half a day range loads minute data
        if range <  12 * 3600 :
            group_level=6

        # one days range loads hourly data
        elif range < 1 * 24 * 3600 :
            group_level=5

        # one month range loads daily data
        elif range < 31 * 24 * 3600 :
            group_level=4

        # one year range loads monthly data
        elif range < 15 * 31 * 24 * 3600 :
            group_level=3

        # greater range loads monthly data
        else:
            group_level=3

    #all_values = getview.get_view_node_id_attribute_json('[fdf5:5351:1dfd:42::2]', 'total_cpu_usage')
        all_values = getview.get_view_nodes_cpu_stat(node_id="[fdf5:5351:1dfd:58::2]",start_timestamp=start_timestamp,end_timestamp=end_timestamp,group_level=group_level)

    else:
        all_values = getview.get_view_nodes_cpu_stat(node_id="[fdf5:5351:1dfd:58::2]",group_level=5)

    json_value = json.dumps(all_values)
    print "group level: "+ str(group_level)

    return HttpResponse(json_value, content_type= "application/json")


def indexgc(request):

    server_ip = util.SERVER_IP
    server_port = util.SERVER_PORT

    all_values = getview.get_view_all_nodes_most_recent()
    all_synthesized_values = getview.get_view_all_nodes_synthesized_most_recent()

#    nodes = constants.nodes
#    for node in nodes:
#        if(node not in nodes_exist):
#            count+=1
#            name = node
#
#            disk_size = None
#            load_avg_1min = None
#            free_mem = None
#            uptime_secs = None
#            last_updated = None
#            total_memory = None
#            num_cpu = None
#            cpu_usage = None
#            data_sent= None
#            data_received = None
#            uptime = None
#            ping_status = None
#            port_status = None
#
#            ping_status = getview.get_view_node_id_synthesized_attribute_most_recent(node,"ping_status")
#            port_status = getview.get_view_node_id_synthesized_attribute_most_recent(node,"port_status")
#
#            all_values.append({'num_cpu': num_cpu, 'percent_usage': cpu_usage ,
#                           'last_updated': last_updated ,'serial':count, 'name':name, 'total_memory': total_memory ,
#                           'disk_size':disk_size, 'load_avg_1min':load_avg_1min, 'free_mem':free_mem, 'data_sent':data_sent,
#                           'data_received':data_received, 'uptime':uptime})


    return render_to_response('index.html',{'all_values':all_values,'all_synthesized_values':all_synthesized_values,
                                              'server_ip': server_ip, 'server_port': server_port },
        context_instance=RequestContext(request))



def node_info_treemap(request, parameter):
    server_ip = util.SERVER_IP
    server_port = util.SERVER_PORT

    metric, arguments = parameter.split('/')

    arg_dict = util.split_arguments_return_dict(arguments)


    all_values = getview.get_view_all_nodes_average_attribute_treemap(arg_dict['limit'])

    values_treemap_cpu = all_values.cpu_usage
    values_treemap_mem_used = all_values.memory_usage
    values_treemap_data_sent = all_values.data_sent
    values_treemap_data_received = all_values.data_received

    #Send as JSON objects
    values_treemap_cpu= json.dumps(values_treemap_cpu)
    values_treemap_mem_used =json.dumps(values_treemap_mem_used)
    values_treemap_data_sent = json.dumps(values_treemap_data_sent)
    values_treemap_data_received = json.dumps(values_treemap_data_received)

    return render_to_response('node_treemap.html', {'values_treemap_cpu':values_treemap_cpu,
                                                    'values_treemap_mem_used':values_treemap_mem_used,
                                                    'values_treemap_data_sent':values_treemap_data_sent,
                                                    'values_treemap_data_received': values_treemap_data_received,
                                                    'server_ip': server_ip, 'server_port': server_port,
                                                    'metric':metric, 'arguments':arg_dict}, context_instance=RequestContext(request))


def node_info_timeline(request, parameter):

    all_values = []
    server_ip = util.SERVER_IP
    server_port = util.SERVER_PORT

    metric, node_id, arguments = parameter.split('/')

    arg_dict = util.split_arguments_return_dict(arguments)

    value = 'web.metricvalue.' + metric

    values_graph = getview.get_view_node_id_attribute_timeline(node_id, metric, start_time =arg_dict['start_time_epoch'],
                                                               end_time=arg_dict['end_time_epoch'], limit=arg_dict['limit'])

    #values_graph = json.dumps(values)
    return render_to_response('node_info_timeline.html',{ 'name':node_id, 'value': eval(value), 'metric':metric,
                                                          'server_ip': server_ip, 'server_port': server_port, 'values_graph':values_graph, 'arguments':arg_dict}
        ,context_instance=RequestContext(request))



def node_info_set_timeline(request, parameter):
    '''
     Parameter received as (metric/node_name.network.interface_name.attribute/start_time0=...)
    '''
    server_ip = util.SERVER_IP
    server_port = util.SERVER_PORT

    (metric_nodeid, resource, resource_spec1, attribute_arguments) = string.split(parameter, '.')

    metric, node_id = metric_nodeid.split("/")
    attribute, arguments = attribute_arguments.split("/")

    parameter = metric_nodeid+'.'+resource+'.'+resource_spec1+'.'+attribute

    value_type= resource+"."+resource_spec1+"."+attribute


    arg_dict = util.split_arguments_return_dict(arguments)

    values_graph = getview.get_view_node_id_attribute_timeline(node_id, value_type, start_time =arg_dict['start_time_epoch'],
                                                                end_time=arg_dict['end_time_epoch'], limit=arg_dict['limit'])


    #values_graph = json.dumps(values)
    return render_to_response('node_info_set_timeline.html',{ 'name':node_id, 'value': resource_spec1+" "+attribute,
                                                          'server_ip': server_ip, 'server_port': server_port,
                                                          'parameter':parameter,  'arguments':arg_dict, 'values_graph':values_graph},context_instance=RequestContext(request))


def node_slivers (request, parameter):

    server_ip = util.SERVER_IP
    server_port = util.SERVER_PORT

    all_values = []
    values_graph = []
    network_values = []
    disk_values = []
    memory_values=[]
    node_in_db = False
    name= parameter

    node_id = parameter
    document = fetchdocument.fetch_most_recent_document(node_id)
    slivers = documentparser.get_value(document, 'slivers')

    count = 0
    if(document):
        node_in_db = True
        for container in slivers:
            sliver= slivers[container]
            count +=1
            sliver_name = documentparser.get_value(sliver, 'sliver_name')
            sliver_cpu_usage = documentparser.get_value(sliver,'sliver_cpu_usage')
            sliver_slice_name = documentparser.get_value(sliver, 'sliver_slice_name')
            sliver_total_memory = documentparser.get_value(sliver, 'sliver_total_memory')
            sliver_total_memory_free = documentparser.get_value(sliver, 'sliver_total_memory_free')
            sliver_total_memory_percent_used = documentparser.get_value(sliver, 'sliver_total_memory_percent_used')

            sliver_total_memory, sliver_total_memory_free = util.convert_bytes_to_human_readable([sliver_total_memory, sliver_total_memory_free])

            all_values.append({'sliver_name': sliver_name, 'sliver_cpu_usage':sliver_cpu_usage, 'sliver_slice_name':sliver_slice_name,
                           'sliver_total_memory':sliver_total_memory, 'sliver_total_memory_free': sliver_total_memory_free,
                           'sliver_total_memory_percent_used':sliver_total_memory_percent_used, 'serial':count})


             # Populate Treemap graph
            values = getview.get_view_sliver_most_recent_attribute_treemap( node_id, 'sliver_cpu_usage')
            values_graph = json.dumps(values)


            #Network Values
            name = documentparser.get_value(document, "name")
            network_values= documentparser.get_set(document, "network")

            #Disk Values
            name = documentparser.get_value(document, "name")
            disk_values= documentparser.get_set(document, "disk")

            #Disk Values
            name = documentparser.get_value(document, "name")
            memory_values= documentparser.get_set(document, "memory")

    return render_to_response('node_slivers.html',{'disk_values':disk_values, 'all_values':all_values,
                                                   'values_graph':values_graph, 'network_values':network_values,
                                                   'name':name, 'server_ip': server_ip, 'server_port': server_port,
                                                   'numberslivers': count, 'node_in_db':node_in_db, 'memory_values': memory_values},
                                                    context_instance=RequestContext(request))



def slice_info(request, parameter):
    all_values = []

    server_ip = util.SERVER_IP
    server_port = util.SERVER_PORT


    slice_id = parameter
    slivers = getview.get_view_slice_id_all_slivers_most_recent(slice_id)

    count = 0
    for container in slivers:
        sliver= container
        count +=1
        sliver_name = documentparser.get_value(sliver, 'sliver_name')
        sliver_cpu_usage = documentparser.get_value(sliver,'sliver_cpu_usage')
        sliver_slice_name = documentparser.get_value(sliver, 'sliver_slice_name')
        sliver_total_memory = documentparser.get_value(sliver, 'sliver_total_memory')
        sliver_total_memory_free = documentparser.get_value(sliver, 'sliver_total_memory_free')
        sliver_total_memory_percent_used = documentparser.get_value(sliver, 'sliver_total_memory_percent_used')
        nodeid = documentparser.get_value(sliver, "nodeid")

        sliver_total_memory, sliver_total_memory_free = util.convert_bytes_to_human_readable([sliver_total_memory, sliver_total_memory_free])

        all_values.append({'sliver_name': sliver_name, 'sliver_cpu_usage':sliver_cpu_usage, 'sliver_slice_name':sliver_slice_name,
                           'sliver_total_memory':sliver_total_memory, 'sliver_total_memory_free': sliver_total_memory_free,
                           'sliver_total_memory_percent_used':sliver_total_memory_percent_used, 'serial':count, 'nodeid': nodeid})


    # Populate Treemap graph
    values = getview.get_view_slice_most_recent_attribute_treemap( slice_id, 'sliver_cpu_usage')
    values_graph = json.dumps(values)


    return render_to_response('sliceinfo.html',{'server_ip': server_ip, 'server_port': server_port,'all_values':all_values, 'values_graph': values_graph},context_instance=RequestContext(request))




def sliver_cpu_usage(request, parameter):

    all_values = []
    sliver_id = parameter
    values_graph = getview.get_view_sliver_id_attribute_timeline(sliver_id, "sliver_cpu_usage")
    #values_graph = json.dumps(values)
    return render_to_response('sliver_info_timeline.html',{ 'name':sliver_id, 'metric': 'CPU Usage (%)', 'values_graph':values_graph},context_instance=RequestContext(request))

def sliver_memory_usage(request, parameter):

    all_values = []
    sliver_id = parameter
    values_graph = getview.get_view_sliver_id_attribute_timeline(sliver_id, "sliver_total_memory_used")
    #values_graph = json.dumps(values)
    return render_to_response('sliver_info_timeline.html',{ 'name':sliver_id, 'metric': 'Memory used', 'values_graph':values_graph},context_instance=RequestContext(request))



def node_ping(request, parameter):

    all_values = []
    node_id = parameter
    all_values = getview.get_view_node_id_synthesized_attribute_timeline(node_id, "ping_status")
    #values_graph = json.dumps(values)
    return render_to_response('synthesized_status.html',{ 'name':node_id, 'metric': 'Ping Status', 'all_values':all_values},context_instance=RequestContext(request))
