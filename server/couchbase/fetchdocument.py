import ast
from couchbase.client import Couchbase
from server.couchbase import store
from server.couchbase import util

def fetch_most_recent_document(node_id):
    db = store.get_bucket()
    most_recent_timestamp = fetch_most_recent_timestamp(node_id,db)
    doc_id = str (node_id) + "-" + str(most_recent_timestamp)
    document = ast.literal_eval(db[doc_id][2])
    return document


# fetch from reference document
def fetch_most_recent_timestamp(node_id, db):
    doc_id = str(node_id) +"-most_recent_timestamp"
    document = ast.literal_eval(db[doc_id][2])
    most_recent_timestamp = document ["most_recent_timestamp"]
    return most_recent_timestamp

if __name__ == '__main__':
    print fetch_most_recent_document(util.IP)
