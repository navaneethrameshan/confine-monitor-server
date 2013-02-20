import time
from server.process import store, util, fetchdocument
from server.process import documentparser


def get_view_node_id_attribute( node_id, value_type):
    #for given node_id get value_type ordered by time (most recent first)
    db = store.get_db()
    view_by_node_id = db.view('node-timestamp/get_node-timestamp', startkey=[node_id,{}], endkey = [node_id], descending = True)


    all_values = [['Time', str(value_type)]]

    all_values = []

    for node in view_by_node_id:
        document = node['value']
        value = documentparser.get_value(document, value_type)
        server_time = documentparser.return_server_time(document)
        all_values.insert(1,[server_time,value]) # Keep most recent value at the end of the list to show graph as ascending time line

    return all_values


def get_view_node_id_attribute_timeline( node_id, value_type):

    #for given node_id get value_type ordered by time (most recent first)
    db = store.get_db()
    view_by_node_id = db.view('node-timestamp/get_node-timestamp', startkey=[node_id,{}], endkey = [node_id,], descending = True, limit= 1000)

    all_values = []

    for node in view_by_node_id:
        document = node['value']
        value = documentparser.get_value(document, value_type)
        server_timestamp = documentparser.return_server_timestamp(document)
        date_time_value= util.convert_epoch_to_date_time_javascript(server_timestamp)
        date_time_value.update({'value': value})
        all_values.insert(1, date_time_value) # Keep most recent value at the end of the list to show graph as ascending time line

    return all_values


def get_view_slice_id_attribute( slice_id, value_type):
    #for given node_id get value_type ordered by time (most recent first)
    db = store.get_db()
    view_by_slice_id = db.view('slice-timestamp/get_slice-timestamp', startkey=[slice_id,{}], endkey = [slice_id], descending = True)


    all_values = [['Time', str(value_type), 'Sliver_ID']]

    all_values = []

    for slice in view_by_slice_id:
        document = slice['value']
        value = documentparser.get_value(document, value_type)
        server_time = documentparser.return_server_time(document)
        sliver_id = documentparser.get_value(document, 'sliver_name')
        all_values.insert(1,[server_time,value, sliver_id]) # Keep most recent value at the end of the list to show graph as ascending time line

    return all_values


def get_view_slice_id_attribute_timeline( slice_id, value_type):
    #for given node_id get value_type ordered by time (most recent first)
    db = store.get_db()
    view_by_slice_id = db.view('slice-timestamp/get_slice-timestamp', startkey=[slice_id,{}], endkey = [slice_id], descending = True)

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

    db = store.get_db()
    view_by_sliver_id = db.view('sliver-timestamp/get_sliver-timestamp', startkey=[sliver_id,{}], endkey = [sliver_id], descending = True)

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

    all_values = [['Id', 'parent', 'metricvalue'], [value_type, '', 0]]

    document = fetchdocument.fetch_most_recent_document(node_id)
    slivers = document['slivers']

    for container in slivers:
        sliver = slivers[container]
        sliver_id = documentparser.get_value(sliver, 'sliver_name')
        value = documentparser.get_value(sliver, value_type)
        all_values.append([sliver_id, value_type, value])

    return all_values


def get_view_slice_id_all_slivers_most_recent( slice_id):
    '''
    Returns a list of the most recent values of all sliver information of a particular slice
    EX: [{sliverid:1,... }, {sliverid:2,... }, ...{sliverid:n, ...}]
    '''

    db = store.get_db()

    #TODO:###################################################
    # The limit value is hardcoded to 5. This value should be obtained from the controller API. It is equal to the number of slivers in the given sliceID
    view_by_slice_id = db.view('slice-timestamp/get_slice-timestamp', startkey=[slice_id,{}], endkey = [slice_id], descending = True, limit=5)

    #########################################################

    all_values = []

    for slice in view_by_slice_id:
        document = slice['value']
        all_values.append(document)

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