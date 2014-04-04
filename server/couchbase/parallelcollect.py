import os
import Queue
import threading
import urllib2
from server import logger
from server.scan import scan

class Parallel_collect(threading.Thread):


    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.log = logger.logger("Parallel Collect")


    def run(self):
        while True:

            # gets the node objects from the queue
            node = self.queue.get()

            node.collect_store()

            node.parse_store()


            # send a signal to the queue that the job is done
            self.queue.task_done()

class Parallel_collect_synthesized(threading.Thread):


    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.log = logger.logger("Parallel Collect synthesized")


    def run(self):
        while True:
            # gets the node objects from the queue
            nodeip6 = self.queue.get()

            value = scan.probe_and_store(nodeip6)

            # send a signal to the queue that the job is done
            self.queue.task_done()


class Parallel_collect_trace(threading.Thread):


    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.log = logger.logger("Parallel Collect Network trace")


    def run(self):
        while True:
            # gets the node objects from the queue
            node = self.queue.get()

            node.collect_store()

            node.parse_store()

            # send a signal to the queue that the job is done
            self.queue.task_done()
