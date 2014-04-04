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