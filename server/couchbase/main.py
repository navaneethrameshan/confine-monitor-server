from common.schedule import Schedule
import store
from server.couchbase import util, collect
from server.couchbase.views import createview


def start_collecting():
    sched = Schedule(util.TIMEPERIOD)
    sched.schedule_couchbase()

def create_view():

    map_function1 = "function(doc) { \
        if ('nodeid' in doc) { \
            node_id = doc.nodeid; \
            timestamp = doc.server_timestamp; \
            emit([node_id,timestamp], doc); \
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

    createview.create_view( 'node-timestamp', map_function1, 'get_node-timestamp')

    createview.create_view( 'slice-timestamp', map_function2, 'get_slice-timestamp')

    createview.create_view( 'sliver-timestamp', map_function3, 'get_sliver-timestamp')

def main():
    store.create_database()
    create_view()
    start_collecting()

if __name__ == "__main__":
    main()
