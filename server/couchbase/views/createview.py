from server.couchbase import store
from server.logger import logger

log = logger("Create View")

def generate_view_document ( doc_name, map_function, view_name, reduce_function=None, reduce=False ):
# check if there are entries for same document_id
    log.debug("Generating view function: %s with Map function as: %s " %(doc_name, map_function))

    if(not reduce):
        design = { 'views': {
            view_name: {
                'map':map_function,
                }
            }
        }
    else:
        design = { 'views': {
            view_name: {
                'map':map_function,
                'reduce': reduce_function
                }
        }
        }

    document_id = '_design/'+ doc_name

    store.store_document(document_id, design)


def create_view():

    log.debug("Creating Views")

    map_function1 = "function(doc) { \
        if(doc.type== 'node'){\
    if ('nodeid' in doc) { \
            node_id = doc.nodeid; \
            timestamp = doc.server_timestamp; \
    emit([node_id,timestamp], null); \
        }\
    }\
    }"

    map_function2 = "function(doc) { \
    if(doc.type== 'node'){\
    if ('slivers' in doc) { \
            slivers = doc.slivers; \
            for (values in slivers){ \
                container = slivers[values]; \
                container['nodeid'] =doc.nodeid;\
                slice = container.slice_name; \
                emit ([slice, doc.nodeid, doc.server_timestamp], container); \
            } \
        } \
        }\
    }"

    map_function3 = "function(doc) { \
    if(doc.type== 'node'){\
    if ('slivers' in doc) { \
            slivers = doc.slivers; \
            for (values in slivers){ \
                container = slivers[values]; \
                container['nodeid'] =doc.nodeid;\
                sliver = container.sliver_name; \
                emit ([sliver, doc.server_timestamp],  {'sliver': container,'nodeid':doc.nodeid,'server_timestamp': doc.server_timestamp}) \
            } \
            }\
    } \
    }"

    map_function4 = "function(doc) { \
       if(doc.type== 'node_synthesized'){\
            node_id = doc.nodeid; \
            timestamp = doc.server_timestamp; \
            emit([node_id,timestamp], null); \
        } \
    }"

    map_function5 = "function (doc, meta) {\
        if(doc.type== 'node_most_recent'){\
            emit(doc.nodeid, null)\
        }\
    }"

    map_function6 = "function (doc, meta) {\
        if(doc.type== 'node_most_recent_synthesized'){\
            emit(doc.nodeid, null)\
        }\
    }"

    map_function7 = "function (doc, meta) {\
        if(doc.type== 'node'){\
            if ('nodeid' in doc) {\
                node_id = doc.nodeid;\
                timestamp = doc.server_timestamp;\
                var date = new Date( timestamp*1000);\
                var dateArray = dateToArray(date);\
                dateArray.splice(0,0,node_id);\
                emit(dateArray, doc.cpu.total_percent_usage);\
            }\
        }\
    }"

    map_function8 = "function (doc, meta) {\
        if(doc.type== 'node'){\
            if ('nodeid' in doc) {\
                node_id = doc.nodeid;\
                timestamp = doc.server_timestamp;\
                var date = new Date( timestamp*1000);\
                var dateArray = dateToArray(date);\
                dateArray.splice(0,0,node_id);\
                emit(dateArray, doc.network.total.bytes_sent_last_sec);\
            }\
        }\
    }"

    map_function9 = "function (doc, meta) {\
        if(doc.type== 'node'){\
            if ('nodeid' in doc) {\
                node_id = doc.nodeid;\
                timestamp = doc.server_timestamp;\
                var date = new Date( timestamp*1000);\
                var dateArray = dateToArray(date);\
                dateArray.splice(0,0,node_id);\
                emit(dateArray, doc.network.total.bytes_recv_last_sec);\
            }\
        }\
    }"

    map_function10 = "function (doc, meta) {\
        if(doc.type== 'node'){\
            if ('nodeid' in doc) {\
                node_id = doc.nodeid;\
                timestamp = doc.server_timestamp;\
                var date = new Date( timestamp*1000);\
                var dateArray = dateToArray(date);\
                dateArray.splice(0,0,node_id);\
                emit(dateArray, doc.memory.virtual.percent_used);\
            }\
        }\
    }"

    reduce_function7 = "_stats"


    generate_view_document( 'node-timestamp', map_function1, 'get_node-timestamp')

    generate_view_document( 'slice-timestamp', map_function2, 'get_slice-timestamp')

    generate_view_document( 'sliver-timestamp', map_function3, 'get_sliver-timestamp')

    generate_view_document( 'synthesized-timestamp', map_function4, 'get_synthesized-timestamp')

    generate_view_document( 'node-mostrecent', map_function5, 'get_node-mostrecent')

    generate_view_document( 'node-synthesized-mostrecent', map_function6, 'get_node-synthesized-mostrecent')

    generate_view_document( 'all_nodes_cpu_stats', map_function7, 'get_all_nodes_cpu_stats', reduce_function7, True)

    generate_view_document( 'all_nodes_bytes_sent', map_function8, 'get_all_nodes_bytes_sent', reduce_function7, True)

    generate_view_document( 'all_nodes_bytes_recv', map_function9, 'get_all_nodes_bytes_recv', reduce_function7, True)

    generate_view_document( 'all_nodes_mem_used', map_function10, 'get_all_nodes_mem_used', reduce_function7, True)
