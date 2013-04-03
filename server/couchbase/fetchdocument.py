import ast
from couchbase.client import Couchbase
from server.couchbase import store
from server.couchbase import util
from server.logger import logger

log = logger("Fetch Document")

def fetch_most_recent_document(node_id):
    log.debug("Fetching most recent document for node: %s" %node_id)
    db = store.get_bucket()
    most_recent_timestamp = fetch_most_recent_timestamp(node_id,db)
    doc_id = str (node_id) + "-" + str(most_recent_timestamp)
    document =  ast.literal_eval(db[doc_id][2])
    log.debug("Document fetched is: " + str(document))
    return document


# fetch from reference document
def fetch_most_recent_timestamp(node_id, db):
    log.debug("Fetching most recent timestamp for node: %s" %node_id)
    doc_id = str(node_id) +"-most_recent_timestamp"
    document = ast.literal_eval(db[doc_id][2])
    most_recent_timestamp = document ["most_recent_timestamp"]
    log.debug("Most recent timestamp fetched is: " + str(most_recent_timestamp))
    return most_recent_timestamp

