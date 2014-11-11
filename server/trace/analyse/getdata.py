from server.couchbase.views import getview
from aggregate import *

def get_all_trace():
    all_trace = getview.get_view_all_nodes_trace()
    print len(all_trace)

    all_path = Paths()

    for node,value in all_trace.items():
       all_path.add_path(value['trace'])
      # print value['trace']

    analyse = Analyse()
    analyse.represent(all_path)

    representation = analyse.get_representation()
    nodes = analyse.get_nodes()

    print str(representation)
    print(nodes)
    return (nodes, representation)

def get_inter_node_trace(nodeid):
    trace = getview.get_view_inter_node_trace(nodeid+'-trace')
    nodes=None
    representation =None

    if trace and trace.has_key('inter-trace'):
        all_path = Paths()
        all_path.add_path(trace['inter-trace'])

        analyse = Analyse()
        analyse.inter_trace_represent(all_path)

        representation = analyse.get_representation()
        nodes = analyse.get_nodes()

    return (nodes, representation)

def get_all_inter_trace():
    all_trace = getview.get_view_all_nodes_inter_trace()

    all_path = Paths()

    for node,value in all_trace.items():
        all_path.add_path(value['inter-trace'])

        # if node == "[fdf5:5351:1dfd:11e::2]":
        #     print value['inter-trace']

    analyse = Analyse()
    analyse.inter_trace_represent(all_path)

    representation = analyse.get_representation()
    nodes = analyse.get_nodes()

    return (nodes, representation)
