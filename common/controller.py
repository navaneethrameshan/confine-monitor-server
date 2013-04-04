import json
import urllib2
from common import nodelist
from server import constants
from server.couchbase import util
from server.logger import logger


log = logger("controller")

def update_node_list():

    nodes =[]

    url = 'http://'+ util.CONTROLLER_IP + '/api/nodes/'
    request = urllib2.Request(url)
    response= None
    try:
        response = urllib2.urlopen(request)
    except:
        log.error("Error in http request")
        response = None

    if(response):
        log.info("Updating Node list from Controller")

        nodes_uri = json.loads(response.read())
        log.debug("Nodes list obtained from controller: "+ str(nodes_uri))
        for dict_node_uri in nodes_uri:
            node_uri= dict_node_uri['uri']
            node_ip6= get_node_ip_from_node_uri(node_uri)
            log.info("Node IP: " + node_ip6)
            if (node_ip6):
                nodes.append(node_ip6)

        nodelist.write_node_list(nodes)




def get_node_ip_from_node_uri(node_uri):

    request = urllib2.Request(node_uri)
    response= None
    try:
        response = urllib2.urlopen(request)
    except:
        log.error("Error in http request")
        response = None

    if(response):
        node_info = json.loads(response.read())
        log.debug("Node Info from controller: "+ str(node_info))
        node_mgmt_net = node_info['mgmt_net']
        node_ip6 = node_ip6='['+node_mgmt_net['addr'] +']'
        return node_ip6

    return None

