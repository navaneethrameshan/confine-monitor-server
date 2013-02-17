import time
from server.process import store, util
from server.process import documentparser


def get_view_node_id_attribute( node_id, value_type):
    #for given node_id get load_avg_1min ordered by time (most recent first)
    db = store.get_db()
    view_by_node_id = db.view('node-timestamp/get_node-timestamp', startkey=[node_id,{}], endkey = [node_id], descending = True)


    all_values = [['Time', str(value_type)]]

    for node in view_by_node_id:
        document = node['value']
        value = documentparser.get_value(document, value_type)
        server_time = documentparser.return_server_time(document)
        all_values.insert(1,[server_time,value]) # Keep most recent value at the end of the list to show graph as ascending time line

    return all_values


def main():
    db = store.get_db()

#    map_function = "function(doc) { \
#        load_avg = doc.load_avg; \
#        load_avg_1min = load_avg['LoadAvg-1min']; \
#        emit([load_avg_1min,doc.server_timestamp], doc); \
#        }"
#
#    create_view(db, 'loadavglist', map_function, 'get_load_avg'  )

###############################################################################################

#    map_function1 = "function(doc) { \
#        if ('nodeid' in doc) { \
#            node_id = doc.nodeid; \
#            timestamp = doc.server_timestamp; \
#            emit([node_id,timestamp], doc); \
#        }\
#    }"
#
#    create_view(db, 'node-timestamp', map_function1, 'get_node-timestamp')

#get_view_node_id_load_avg('127.0.0.1')

if __name__ == "__main__" :
    main()