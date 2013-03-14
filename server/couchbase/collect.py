from server.couchbase import store
from server.couchbase import util
from server import rename
from server.couchbase import documentparser
from server.logger import logger


import urllib2
import json

log = logger("Collect")

class Collect:

# TODO: IP, PORT,Last_seen_sequence_number  needs to be read from class variable. Currently fetching from util for testing

    def __init__(self, name, sequence = 0):

        self.name = name
        self.sequence= sequence
        self.value= {}

    def generate_url(self):
    # Need to absolutely ensure that the same sequence number values are never fetched twice. This will most likely result in a collision and resource conflict on updating the database.
        request_url = 'http://'+ util.IP +':' + util.PORT + "/get/all/seqnumber=" + str(self.sequence)
        return request_url

    def generate_reference_docid(self, node_id):
        doc_id = node_id +'-most_recent_timestamp'
        return doc_id

    def collect(self):

        # Possibility to optimize here by maintaining tcp connection? urllib3 and httpconnectionpool or httplib. Also important for
        # handling cases of out of order message arrival. Although out of order messages shouldn't ideally affect anything.
        url = self.generate_url()
        log.info(url)
        request = urllib2.Request(url)
        response= None
        try:
            response = urllib2.urlopen(request)
        except:
            log.error("Error in http request")
            response = None


        if(response is None):
            return None

        page = json.loads(response.read())

        #get and update the last seen sequence number
        sequence = util.get_most_recent_sequence_number(page)
        self.sequence = sequence #Wouldn't work if the server crashes. Need to persist??

        # print sequence
        return page


    def parse_store(self):
        log.info("NODE ID: " + self.name)
        db = store.get_bucket()
        most_recent_absolute_timestamp = 0.0

        if (self.value is None):
            return

         #parse the dictionary. Strip values of every sequence number and add nodeid, absolute server timestamp
        for key in self.value.keys():
            seq_value = self.value[key]
            seq_value.update({'nodeid': self.name})
            seq_value.update({'seq': key})

            ###########################TODO: Testing for generated Sliver and Slice ID. Remove later####################

            rename.rename_sliver(seq_value, self.name)

            ############################################################################################################

            #convert the relative timestamp to absolute server timestamp. Relative timestamps and server receiving the requests are always causally ordered.
            server_absolute_timestamp = util.get_timestamp()- float (seq_value['relative_timestamp'])
            seq_value.update({'server_timestamp': server_absolute_timestamp})

            most_recent_absolute_timestamp = util.find_recent_timestamp(most_recent_absolute_timestamp, server_absolute_timestamp)

            # should only fetch the document timestamp and not generate a new one
            # print str(server_absolute_timestamp) + "--" + str(key) + "-- time" + str(config.get_timestamp())
            doc_id = self.generate_docid(self.name, server_absolute_timestamp)
            store.store_document(doc_id,seq_value)

        # After all the documents are stored, find the most recent timestamp and update the reference document to speedup lookups
        reference_doc_id = self.generate_reference_docid(self.name)
        store.update_document(reference_doc_id, {"most_recent_timestamp": most_recent_absolute_timestamp})


    def collect_store(self):
        self.value = self.collect()


    def generate_docid(self, node_id, timestamp):
        doc_id = node_id +'-'+str(timestamp)
        return doc_id

    def get_name(self):
        return self.name