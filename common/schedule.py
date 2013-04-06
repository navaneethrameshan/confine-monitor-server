from Queue import Queue
from threading import Thread
import time
import sys
from common import controller, nodelist
from server import constants
from server.couchbase.collect import Collect as couchbasecollect
from server.logger import logger
from server.couchbase import parallelcollect, util

class Schedule:

    def __init__(self, time_period):
        self.time_period = time_period
        self.log = logger("Schedule")
        self.q= Queue()
        self.node_ip6q = Queue()

    def schedule_couchbase (self):

        self.node_list= []

        #update node list from controller
        controller.update_node_list()

        nodes = nodelist.get_node_list()

        for name in nodes:
            self.node_list.append(couchbasecollect(name, port = util.RD_PORT))

        self.log.info("Number of Nodes: %d" %len(nodes) )
	
	for i in range(len(nodes)):
                t1= parallelcollect.Parallel_collect(self.q)
                t1.daemon=True
                t1.start()
                t2= parallelcollect.Parallel_collect_synthesized(self.node_ip6q)
                t2.daemon= True
                t2.start()


        while(1):

            try:
                for node in self.node_list:
                    self.q.put(node)

                for nodeip6 in nodes:
                    self.node_ip6q.put(nodeip6)

                self.q.join()
                self.node_ip6q.join()
            except KeyboardInterrupt:
                sys.exit(1)

            time.sleep(self.time_period)
            self.log.info("Scheduling next run")

