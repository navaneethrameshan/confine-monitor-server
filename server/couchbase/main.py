from common.schedule import Schedule
import store
from server.couchbase import util, collect
from server.couchbase.views import createview


def start_collecting():
    sched = Schedule(util.TIMEPERIOD)
    sched.schedule_couchbase()



def main():
    store.create_database()
    createview.create_view()
    start_collecting()

if __name__ == "__main__":
    main()
