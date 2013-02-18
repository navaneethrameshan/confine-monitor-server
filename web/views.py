from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context, RequestContext, Template
from django.http import HttpResponse, Http404
import json
import string
from server.process import fetchdocument, util, documentparser
from server.process.views import getview
from server import constants

def index(request):

    server_ip = util.SERVER_IP
    server_port = util.SERVER_PORT

    all_values = []
    count = 0
    # the initial page to display
    for nodes in  constants.nodes:
        count+=1
        document = fetchdocument.fetch_most_recent_document(nodes)
        name = documentparser.get_value(document, "name")
        disk_size = documentparser.get_value(document, "disk_size")
        load_avg_1min = documentparser.get_value(document, "load_avg_1min")
        free_mem = documentparser.get_value(document, "free_memory")
        uptime_secs = documentparser.get_value(document, "uptime")
        last_updated = documentparser.return_server_time(document)
        total_memory = documentparser.get_value(document,"total_memory")
        num_cpu = documentparser.get_value(document, "number_of_cpus")
        cpu_usage = documentparser.get_value(document, "total_cpu_usage")


        ## Human readability######
        uptime = util.convert_secs_to_time(uptime_secs)
        (disk_size,total_memory,free_mem)= util.convert_bytes_to_human_readable([disk_size,total_memory,free_mem])


        all_values.append({'num_cpu': num_cpu, 'percent_usage': cpu_usage , 'server_ip': server_ip, 'server_port': server_port, 'last_updated': last_updated ,'serial':count, 'name':name, 'total_memory': total_memory ,'disk_size':disk_size, 'load_avg_1min':load_avg_1min, 'free_mem':free_mem, 'uptime':uptime})


    #get values for graph
    values = getview.get_view_node_id_attribute('127.0.0.1', "load_avg_1min")

   # Use to strip double quotes and single quotes to pass data for annotated timeline
   # str_values = str(values)
   # modified_string = str_values.replace('\"', ' ').strip().replace("\'", ' ').strip()

    values_graph = json.dumps(values)

    return render_to_response('indexgc.html',{'all_values':all_values},context_instance=RequestContext(request))


def load_avg_1min(request, parameter):

    node_id = parameter
    values_graph = getview.get_view_node_id_attribute_dict(node_id, "load_avg_1min")
   # values_graph = json.dumps(values)
    return render_to_response('node_info_timeline.html',{ 'name':node_id, 'metric': 'Load Average 1 min', 'values_graph':values_graph},context_instance=RequestContext(request))


def cpu_usage(request, parameter):

    all_values = []
    node_id = parameter
    values_graph = getview.get_view_node_id_attribute_dict(node_id, "total_cpu_usage")
    #values_graph = json.dumps(values)
    return render_to_response('node_info_timeline.html',{ 'name':node_id, 'metric': 'CPU Usage (%)', 'values_graph':values_graph},context_instance=RequestContext(request))



def freemem(request, parameter):

    node_id = parameter
    values_graph = getview.get_view_node_id_attribute_dict(node_id, "free_memory")
    #values_graph = json.dumps(values)
    return render_to_response('node_info_timeline.html',{ 'name':node_id, 'metric': 'Free Memory', 'values_graph':values_graph},context_instance=RequestContext(request))

def uptime(request, parameter):

    node_id = parameter
    values_graph = getview.get_view_node_id_attribute_dict(node_id, "uptime")
    #values_graph = json.dumps(values)
    return render_to_response('node_info_timeline.html',{ 'name':node_id, 'metric': 'Uptime', 'values_graph':values_graph},context_instance=RequestContext(request))

