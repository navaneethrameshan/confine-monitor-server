from Queue import Queue
from threading import Thread
import time
import sys
from server import constants
from server.couchbase.collect import Collect as couchbasecollect
from server.logger import logger
from server.couchbase import parallelcollect, util

class Schedule:

    def __init__(self, time_period):
        self.time_period = time_period
        self.log = logger("Schedule")
        self.q= Queue()

    def schedule_couchbase (self):

        self.node_list= []

        for name in constants.nodes:
            self.node_list.append(couchbasecollect(name, port = util.PORT))

        self.log.info("Number of Nodes: %d" %len(constants.nodes) )

        while(1):

            #TODO: Get this value from controller API and not constant.nodes#########
            for i in range(len(constants.nodes)):
                t= parallelcollect.Parallel_collect(self.q)
                t.daemon=True
                t.start()

            try:
                for node in self.node_list:
                    self.q.put(node)

                self.q.join()
            except KeyboardInterrupt:
                sys.exit(1)

            time.sleep(self.time_period)
            self.log.info("Scheduling next run")


