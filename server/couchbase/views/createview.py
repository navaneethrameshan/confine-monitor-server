from server.couchbase import store
from server.logger import logger

log = logger("Create View")

def generate_view_document ( doc_name, map_function, view_name ):
# check if there are entries for same document_id
    log.debug("Generating view function: %s with Map function as: %s " %(doc_name, map_function))

    map_load_avg =  map_function

    design = { 'views': {
        view_name: {
            'map':map_load_avg
        }
    } }

    document_id = '_design/'+ doc_name

    store.store_document(document_id, design)


def create_view():

    log.debug("Creating Views")

    map_function1 = "function(doc) { \
        if ('nodeid' in doc) { \
            node_id = doc.nodeid; \
            timestamp = doc.server_timestamp; \
            emit([node_id,timestamp], null); \
        }\
    }"

    map_function2 = "function(doc) { \
        if ('slivers' in doc) { \
            slivers = doc.slivers; \
            for (values in slivers){ \
                container = slivers[values]; \
                container['nodeid'] =doc.nodeid;\
                slice = container.slice_name; \
                emit ([slice, doc.server_timestamp], container); \
            } \
        } \
    }"

    map_function3 = "function(doc) { \
        if ('slivers' in doc) { \
            slivers = doc.slivers; \
            for (values in slivers){ \
                container = slivers[values]; \
                container['nodeid'] =doc.nodeid;\
                sliver = container.sliver_name; \
                emit ([sliver, doc.server_timestamp],  {'sliver': container,'nodeid':doc.nodeid,'server_timestamp': doc.server_timestamp}) \
            } \
        } \
    }"

    generate_view_document( 'node-timestamp', map_function1, 'get_node-timestamp')

    generate_view_document( 'slice-timestamp', map_function2, 'get_slice-timestamp')

    generate_view_document( 'sliver-timestamp', map_function3, 'get_sliver-timestamp')
