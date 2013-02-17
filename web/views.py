from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context, RequestContext, Template
from django.http import HttpResponse, Http404
import json
import string
from server.process import fetchdocument, util, documentparser
from server.process.views import getview

def hello(request):
  #  return HttpResponse("Monitoring Service")
  # return render_to_response('testing.html')
    import urllib2
    import json
    from BeautifulSoup import BeautifulSoup

#Download the graph page using Python's urllib2 from the demo URL
#The URL is shortened for the purposes of this demo.
#Feel free to use this URL for your own testing.
    page = urllib2.urlopen('http://glowfilter.com/media/static/glowfilter/articles/flot-beautiful-soup-demo/world_population.html')

#Create a BeautifulSoup object.
    soup = BeautifulSoup(page)

#Creating some variables to pass to the Django template
    data = ""
    countries = []

#Find all of the table rows
    for row in soup.findAll("tr",{"class":"dataRow"}):
        country = []

    #For each row, get the contents of the relevant cells, and place them into the countries array.
    #This array will be rendered as JSON into the view for populating the Flot graph
        for cell in row.findAll("td",{"class":"year"}):
            country.append(int(cell.contents[0].replace(",","")))
        for cell in row.findAll("td",{"class":"population"}):
            country.append(int(cell.contents[0].replace(",","")))

        countries.append(country)
        print countries

#Transform the countries array into JSON
    data = json.dumps(countries)

#Render the template, with the countries JSON string passed into the template context
    return render_to_response('testing.html',{'countries':data, 'monitor':'navaneeth'},context_instance=RequestContext(request))


def index(request):

    server_ip = util.SERVER_IP
    server_port = util.SERVER_PORT

    # the initial page to display
    document = fetchdocument.fetch_most_recent_document(util.IP)
    name = documentparser.get_value(document, "name")
    disk_size = documentparser.get_value(document, "disk_size")
    load_avg_1min = documentparser.get_value(document, "load_avg_1min")
    free_mem = documentparser.get_value(document, "free_memory")
    uptime_secs = documentparser.get_value(document, "uptime")
    uptime = util.convert_secs_to_time(uptime_secs)
    last_updated = documentparser.return_server_time(document)
    total_memory = documentparser.get_value(document,"total_memory")
    num_cpu = documentparser.get_value(document, "number_of_cpus")
    cpu_usage = documentparser.get_value(document, "total_cpu_usage")

    name = str(name)

    #get values for graph
    values = getview.get_view_node_id_attribute('127.0.0.1', "load_avg_1min")

   # Use to strip double quotes and single quotes to pass data for annotated timeline
   # str_values = str(values)
   # modified_string = str_values.replace('\"', ' ').strip().replace("\'", ' ').strip()

    values_graph = json.dumps(values)

    return render_to_response('indexgc.html',{'num_cpu': num_cpu, 'percent_usage': cpu_usage , 'server_ip': server_ip, 'server_port': server_port, 'last_updated': last_updated ,'serial':1, 'name':name, 'total_memory': total_memory ,'disk_size':disk_size, 'load_avg_1min':load_avg_1min, 'free_mem':free_mem, 'uptime':uptime,'values_graph':values_graph},context_instance=RequestContext(request))


def load_avg_1min(request, parameter):

    node_id = parameter
    values = getview.get_view_node_id_attribute(node_id, "load_avg_1min")
    values_graph = json.dumps(values)
    return render_to_response('node_info.html',{ 'name':node_id, 'metric': 'Load Average 1 min', 'values_graph':values_graph},context_instance=RequestContext(request))


def cpu_usage(request, parameter):

    node_id = parameter
    values = getview.get_view_node_id_attribute(node_id, "total_cpu_usage")
    values_graph = json.dumps(values)
    return render_to_response('node_info.html',{ 'name':node_id, 'metric': 'CPU Usage (%)', 'values_graph':values_graph},context_instance=RequestContext(request))



def freemem(request, parameter):

    node_id = parameter
    values = getview.get_view_node_id_attribute(node_id, "free_memory")
    values_graph = json.dumps(values)
    return render_to_response('node_info.html',{ 'name':node_id, 'metric': 'Free Memory', 'values_graph':values_graph},context_instance=RequestContext(request))

def uptime(request, parameter):

    node_id = parameter
    values = getview.get_view_node_id_attribute(node_id, "uptime")
    values_graph = json.dumps(values)
    return render_to_response('node_info.html',{ 'name':node_id, 'metric': 'Uptime', 'values_graph':values_graph},context_instance=RequestContext(request))

def gtest(request):
    values = {"1": {"time": 10000, "value": 10}, "2": {"time": 20000, "value": 20}}

    return render_to_response('testinggchart.html',{'values_graph':values},context_instance=RequestContext(request))