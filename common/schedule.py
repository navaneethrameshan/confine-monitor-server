import time
import gevent
from gevent import monkey
from server import constants
from server.process.collect import collect

class Schedule:

    def __init__(self, time_period):
            self.time_period = time_period


    def schedule (self):

        monkey.patch_all(thread=False, select=False)
        node_list= []
        for name in constants.nodes:
            node_list.append(collect(name))
        while(1):
            gevent.joinall([gevent.spawn(node.collect_store) for node in node_list])
            for node in node_list:
                node.parse_store()
            time.sleep(self.time_period)
            print "scheduling next run"
