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
        self.trace_node= Queue()

    def schedule_couchbase (self):

        self.node_list= []
        self.trace_node_list = []

        #update node list from controller
        controller.update_node_list()

        nodes = nodelist.get_node_list()
        #Server hanging after a few days could be a possible shelve problem??

        for name in nodes:
           # self.node_list.append(couchbasecollect(name, port = util.RD_PORT, ip= name)) # docid is the same as ip, type = node (default)
            self.trace_node_list.append(couchbasecollect(str(name+'-trace'), port = '8000', ip=name, type='trace-route' )) # docid wouldbe "ip-trace-timestamp", type = trace-route

        self.log.info("Number of Nodes: %d" %len(nodes) )
	
        for i in range(2):
#            t1= parallelcollect.Parallel_collect(self.q)
#            t1.daemon=True
#            t1.start()
#            t2= parallelcollect.Parallel_collect_synthesized(self.node_ip6q)
#            t2.daemon= True
#            t2.start()
            #Add thread to collect network trace info
            t3 = parallelcollect.Parallel_collect_trace(self.trace_node)
            t3.daemon = True
            t3.start()


        while(1):

            try:
#                for node in self.node_list:
#                    self.q.put(node)
#
#                for nodeip6 in nodes:
#                    self.node_ip6q.put(nodeip6)

                for node in self.trace_node_list:
                    self.trace_node.put(node)

#                print("Waiting for Collect Queue!!!")
#                self.q.join()
#                print ("Waiting for synthesized queue!!!")
#                self.node_ip6q.join()
                print ("Waiting for trace queue!!!")
                self.trace_node.join()
                print("Done!!")

            except KeyboardInterrupt:
                sys.exit(1)

            time.sleep(self.time_period)
            self.log.info("---------------------------------------------")
            self.log.info("Scheduling next run")
            self.log.info("---------------------------------------------")

