from couchdb import *
from server.process import store
from server.process import util

def fetch_most_recent_document(node_id):
    db = store.get_db()
    most_recent_timestamp = fetch_most_recent_timestamp(node_id,db)
    doc_id = str (node_id) + "-" + str(most_recent_timestamp)
    document = db[doc_id]
    return document


# fetch from reference document
def fetch_most_recent_timestamp(node_id, db):
    doc_id = str(node_id) +"-most_recent_timestamp"
    document = db[doc_id]
    most_recent_timestamp = document ["most_recent_timestamp"]
    return most_recent_timestamp

if __name__ == '__main__':
    print fetch_most_recent_document(util.IP)
