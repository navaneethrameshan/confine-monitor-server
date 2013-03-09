import time
from server import constants
from server.couchbase.collect import collect as couchbasecollect

class Schedule:

    def __init__(self, time_period):
            self.time_period = time_period


    def schedule_couchbase (self):


        node_list= []

        #TODO: Get this value from controller API#########
        for name in constants.nodes:
            node_list.append(couchbasecollect(name))
            ################################################

        while(1):
            for node in node_list:
                node.collect_store()
                node.parse_store()
            time.sleep(self.time_period)
            print "scheduling next run"
