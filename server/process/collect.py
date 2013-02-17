from server.process import store
from server.process import util

import urllib2
import json


# TODO: IP and PORT needs to be read from the api

def generate_url():
# Need to absolutely ensure that the same sequence number values are never fetched twice. This will most likely result in a collision and resource conflict on updating the database.
    request_url = 'http://'+ util.IP +':' + util.PORT + "/get/all/seqnumber=" + str(util.LAST_SEEN_SEQ_NUMBER)
    return request_url

def generate_reference_docid(node_id):
    doc_id = node_id +'-most_recent_timestamp'
    return doc_id

def collect():

    # Possibility to optimize here by maintaining tcp connection? urllib3 and httpconnectionpool or httplib. Also important for
    # handling cases of out of order message arrival.
    url = generate_url()
    request = urllib2.Request(url)
    try:
        response = urllib2.urlopen(request)
    except:
        print "Error in http request "

    page = json.loads(response.read())

    #get and update the last seen sequence number
    sequence = util.get_most_recent_sequence_number(page)
    util.LAST_SEEN_SEQ_NUMBER = sequence  #Wouldn't work if the server crashes. Need to persist??

   # print sequence
    return page


def parse_store(value, db):

    most_recent_absolute_timestamp = 0.0

#parse the dictionary. Strip values of every sequence number and add nodeid, absolute server timestamp
    for key in value.keys():
        seq_value = value[key]
        seq_value.update({'nodeid': util.IP})
        seq_value.update({'seq': key})
 #convert the relative timestamp to absolute server timestamp. Relative timestamps and server receiving the requests are always causally ordered.
        server_absolute_timestamp = util.get_timestamp()- float (seq_value['relative_timestamp'])
        seq_value.update({'server_timestamp': server_absolute_timestamp})

        most_recent_absolute_timestamp = util.find_recent_timestamp(most_recent_absolute_timestamp, server_absolute_timestamp)

# should only fetch the document timestamp and not generate a new one
       # print str(server_absolute_timestamp) + "--" + str(key) + "-- time" + str(config.get_timestamp())
        doc_id = generate_docid(util.IP, server_absolute_timestamp)
        store.store_document(doc_id,seq_value, db)

# After all the documents are stored, find the most recent timestamp and update the reference document to speedup lookups
    reference_doc_id = generate_reference_docid(util.IP)
    store.update_document(reference_doc_id, {"most_recent_timestamp": most_recent_absolute_timestamp},db)


def create_document():
    value= {}
    value = collect()

    db = store.get_db()
    parse_store(value, db)


def generate_docid(node_id, timestamp):
    doc_id = node_id +'-'+str(timestamp)
    return doc_id


def request_store():
    create_document()


def main():
    request_store()
   # collect()

if __name__ == "__main__":
    main()