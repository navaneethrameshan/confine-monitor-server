# First we import the Fabric api
from fabric.api import *
import json
import urllib2
import shelve
import os
import socket, paramiko
import multiscp

nodes = []

def update_node_list():
    url = 'http://controller.confine-project.eu/api/nodes/'
    request = urllib2.Request(url)
    response= None
    try:
        response = urllib2.urlopen(request)
    except:
        response = None
    if(response):
        nodes_uri = json.loads(response.read())
        for dict_node_uri in nodes_uri:
            node_uri= dict_node_uri['uri']
            node_ip6= get_node_ip_from_node_uri(node_uri)
            if (node_ip6):
                nodes.append(node_ip6)
    write_node_list(nodes)



def get_node_ip_from_node_uri(node_uri):
    request = urllib2.Request(node_uri)
    response= None
    try:
        response = urllib2.urlopen(request)
    except:
        response = None
    if(response):
        node_info = json.loads(response.read())
        node_mgmt_net = node_info['mgmt_net']
        node_ip6 = node_ip6='['+node_mgmt_net['addr'] +']'
        return node_ip6
    return None


def write_node_list(nodes):
    s = shelve.open('node_list_shelf.db', writeback = True)
    try:
        s['node_list']= nodes
    finally:
        s.close()


def get_node_list():
    nodes=[]
    s = shelve.open('node_list_shelf.db', writeback = True)
    try:
        if('node_list' in s):
            nodes = s['node_list']
    finally:
        s.close()
    return nodes


if __name__ =='__main__':
    path= os.path.join(os.path.dirname(__file__), 'node_list_shelf.db')
    if(os.path.exists(path)):
        os.remove(path)
    update_node_list()
    nodes= get_node_list()
    for node in nodes:
        dest = 'root@'+node
        print dest
        multiscp.scp(['/home/navaneeth/PycharmProjects/confine_monitor/'], dest)




# We can then specify host(s) and run the same commands across those systems
env.user = 'root'
env.password = 'confine'
env.hosts = get_node_list()
env.warn_only = True

def runserver():
    if _is_host_up(env.host, int(env.port)) is True:
        with cd("confine_monitor"):
            run("python runserver.py &", pty=False)

def runmonitor():
    if _is_host_up(env.host, int(env.port)) is True:
        with cd("confine_monitor"):
            run("python main.py &", pty=False)

def uptime():
    if _is_host_up(env.host, int(env.port)) is True:
        run("uptime")

def _is_host_up(host, port):
    # Set the timeout
    original_timeout = socket.getdefaulttimeout()
    new_timeout = 10
    socket.setdefaulttimeout(new_timeout)
    host_status = False
    try:
        transport = paramiko.Transport((host, port))
        host_status = True
    except:
        print('***Warning*** Host {host} on port {port} is down.'.format(
            host=host, port=port)
            )
    socket.setdefaulttimeout(original_timeout)
    return host_status