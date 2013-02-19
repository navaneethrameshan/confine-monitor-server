from common.schedule import Schedule
import store
from server.process import util, collect
from server.process.views import createview


def start_collecting():
    sched = Schedule(util.TIMEPERIOD)
    sched.schedule()

def create_view():
    db = store.get_db()
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

    createview.create_view(db, 'node-timestamp', map_function1, 'get_node-timestamp')

    createview.create_view(db, 'slice-timestamp', map_function2, 'get_slice-timestamp')

def main():
    create_view()
    start_collecting()

if __name__ == "__main__":
    main()
