from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context, RequestContext, Template
from django.http import HttpResponse, Http404
import json
import string
from common import nodelist
from server.couchbase import fetchdocument, util, documentparser
from server.couchbase.views import getview
from server import constants

def index(request):

    server_ip = util.SERVER_IP
    server_port = util.SERVER_PORT

    all_values = []
    count = 0
    # the initial page to display
    nodes = nodelist.get_node_list()

    for node in nodes:
        count+=1

        document = fetchdocument.fetch_most_recent_document(node)
        name = documentparser.get_value(document, "name")
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


        ping_status = getview.get_view_node_id_synthesized_attribute_most_recent(node,"ping_status")
        port_status = getview.get_view_node_id_synthesized_attribute_most_recent(node,"port_status")

        ## Human readability######
        uptime = util.convert_secs_to_time(uptime_secs)
        disk_size,total_memory,free_mem,data_sent, data_received = util.convert_bytes_to_human_readable([disk_size,total_memory,free_mem, data_sent, data_received])


        all_values.append({'num_cpu': num_cpu, 'percent_usage': cpu_usage , 'server_ip': server_ip, 'server_port': server_port,
                           'last_updated': last_updated ,'serial':count, 'name':name, 'total_memory': total_memory ,
                           'disk_size':disk_size, 'load_avg_1min':load_avg_1min, 'free_mem':free_mem, 'data_sent':data_sent,
                           'data_received':data_received, 'uptime':uptime, 'ping_status':ping_status, 'port_status':port_status})


   # Use to strip double quotes and single quotes to pass data for annotated timeline
   # str_values = str(values)
   # modified_string = str_values.replace('\"', ' ').strip().replace("\'", ' ').strip()

    return render_to_response('indexgc.html',{'all_values':all_values},context_instance=RequestContext(request))


def load_avg_1min(request, parameter):

    node_id = parameter
    values_graph = getview.get_view_node_id_attribute_timeline(node_id, "load_avg_1min")
   # values_graph = json.dumps(values)
    return render_to_response('node_info_timeline.html',{ 'name':node_id, 'metric': 'Load Average 1 min', 'values_graph':values_graph},context_instance=RequestContext(request))


def cpu_usage(request, parameter):

    all_values = []
    node_id = parameter
    values_graph = getview.get_view_node_id_attribute_timeline(node_id, "total_cpu_usage")
    #values_graph = json.dumps(values)
    return render_to_response('node_info_timeline.html',{ 'name':node_id, 'metric': 'CPU Usage (%)', 'values_graph':values_graph},context_instance=RequestContext(request))



def free_mem(request, parameter):

    node_id = parameter
    values_graph = getview.get_view_node_id_attribute_timeline(node_id, "free_memory")
    #values_graph = json.dumps(values)
    return render_to_response('node_info_timeline.html',{ 'name':node_id, 'metric': 'Free Memory', 'values_graph':values_graph},context_instance=RequestContext(request))

def uptime(request, parameter):

    node_id = parameter
    values_graph = getview.get_view_node_id_attribute_timeline(node_id, "uptime")
    #values_graph = json.dumps(values)
    return render_to_response('node_info_timeline.html',{ 'name':node_id, 'metric': 'Uptime', 'values_graph':values_graph},context_instance=RequestContext(request))

def data_sent(request, parameter):

    node_id = parameter
    values_graph = getview.get_view_node_id_attribute_timeline(node_id, "network_total_bytes_sent_last_sec")
    #values_graph = json.dumps(values)
    return render_to_response('node_info_timeline.html',{ 'name':node_id, 'metric': 'Total Bytes sent/Sec', 'values_graph':values_graph},context_instance=RequestContext(request))

def data_received(request, parameter):

    node_id = parameter
    values_graph = getview.get_view_node_id_attribute_timeline(node_id, "network_total_bytes_received_last_sec")
    #values_graph = json.dumps(values)
    return render_to_response('node_info_timeline.html',{ 'name':node_id, 'metric': 'Total Bytes received/Sec', 'values_graph':values_graph},context_instance=RequestContext(request))


def network_timeline(request, parameter):
    '''
     Parameter received as (node_name.network.interface_name.attribute)
    '''
    (node_id, network, interface, attribute) = string.split(parameter, '.')
    value_type= network+"."+interface+"."+attribute
    values_graph = getview.get_view_node_id_attribute_timeline(node_id, value_type)
    #values_graph = json.dumps(values)
    return render_to_response('node_info_timeline.html',{ 'name':node_id, 'metric': interface+" "+attribute, 'values_graph':values_graph},context_instance=RequestContext(request))


def disk_timeline(request, parameter):
    '''
     Parameter received as (node_name.network.interface_name.attribute)
    '''
    (node_id, disk, partition, attribute) = string.split(parameter, '.')
    value_type= disk+"."+partition+"."+attribute
    values_graph = getview.get_view_node_id_attribute_timeline(node_id, value_type)
    #values_graph = json.dumps(values)
    return render_to_response('node_info_timeline.html',{ 'name':node_id, 'metric': partition+" "+attribute, 'values_graph':values_graph},context_instance=RequestContext(request))


def node_slivers (request, parameter):

    server_ip = util.SERVER_IP
    server_port = util.SERVER_PORT

    all_values = []

    node_id = parameter
    document = fetchdocument.fetch_most_recent_document(node_id)
    slivers = documentparser.get_value(document, 'slivers')

    count = 0
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

    return render_to_response('node_slivers.html',{'disk_values':disk_values, 'all_values':all_values, 'values_graph':values_graph, 'network_values':network_values, 'name':name, 'server_ip': server_ip, 'server_port': server_port, 'numberslivers': count},context_instance=RequestContext(request))



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
                           'sliver_total_memory_percent_used':sliver_total_memory_percent_used, 'serial':count, 'server_ip': server_ip, 'server_port': server_port, 'nodeid': nodeid})


    # Populate Treemap graph
    values = getview.get_view_slice_most_recent_attribute_treemap( slice_id, 'sliver_cpu_usage')
    values_graph = json.dumps(values)


    return render_to_response('sliceinfo.html',{'all_values':all_values, 'values_graph': values_graph},context_instance=RequestContext(request))




def sliver_cpu_usage(request, parameter):

    all_values = []
    sliver_id = parameter
    values_graph = getview.get_view_sliver_id_attribute_timeline(sliver_id, "sliver_cpu_usage")
    #values_graph = json.dumps(values)
    return render_to_response('node_info_timeline.html',{ 'name':sliver_id, 'metric': 'CPU Usage (%)', 'values_graph':values_graph},context_instance=RequestContext(request))

def sliver_memory_usage(request, parameter):

    all_values = []
    sliver_id = parameter
    values_graph = getview.get_view_sliver_id_attribute_timeline(sliver_id, "sliver_total_memory_used")
    #values_graph = json.dumps(values)
    return render_to_response('node_info_timeline.html',{ 'name':sliver_id, 'metric': 'Memory used', 'values_graph':values_graph},context_instance=RequestContext(request))



def node_network(request, parameter):

   node_id = parameter
   document = fetchdocument.fetch_most_recent_document(node_id)
   name = documentparser.get_value(document, "name")
   network_values= documentparser.get_set(document, "network")

   return render_to_response('node_network.html',{'network_values':network_values, "name":name},context_instance=RequestContext(request))

def node_disk(request, parameter):

    node_id = parameter
    document = fetchdocument.fetch_most_recent_document(node_id)
    name = documentparser.get_value(document, "name")
    disk_values= documentparser.get_set(document, "disk")

    return render_to_response('node_disk.html',{'disk_values':disk_values, "name":name},context_instance=RequestContext(request))

def node_cpu(request, parameter):

    node_id = parameter
    document = fetchdocument.fetch_most_recent_document(node_id)
    name = documentparser.get_value(document, "name")
    cpu_values= documentparser.get_set(document, "cpu")

    return render_to_response('node_cpu.html',{'cpu_values':cpu_values, "name":name},context_instance=RequestContext(request))

def node_ping(request, parameter):

    all_values = []
    node_id = parameter
    all_values = getview.get_view_node_id_synthesized_attribute_timeline(node_id, "ping_status")
    #values_graph = json.dumps(values)
    return render_to_response('synthesized_status.html',{ 'name':node_id, 'metric': 'Ping Status', 'all_values':all_values},context_instance=RequestContext(request))
