import os
import Queue
import threading
import urllib2
from server import logger

class Parallel_collect(threading.Thread):
    """Threaded File Downloader"""

    #----------------------------------------------------------------------
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.log = logger.logger("Parallel Collect")

    #----------------------------------------------------------------------
    def run(self):
        while True:
            # gets the node objects from the queue
            node = self.queue.get()

            node.collect_store()

            node.parse_store()

            # send a signal to the queue that the job is done
            self.queue.task_done()

