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

    try:
        str_doc= db[doc_id][2]
    except:
        return {}

    document =  ast.literal_eval(str_doc)
    log.debug("Document fetched is: " + str(document))
    return document


# fetch from reference document
def fetch_most_recent_timestamp(node_id, db):
    log.debug("Fetching most recent timestamp for node: %s" %node_id)
    doc_id = str(node_id) +"-most_recent_timestamp"

    try:
        str_doc= db[doc_id][2]
    except:
        return {}

    document = ast.literal_eval(str_doc)
    most_recent_timestamp = document ["most_recent_timestamp"]
    log.debug("Most recent timestamp fetched is: " + str(most_recent_timestamp))
    return most_recent_timestamp


def fetch_synthesized_data_document(node_id):
    db = store.get_bucket()
    log.debug("Fetching synthesized data document for node: %s" %node_id)
    doc_id = str(node_id) +"-synthesized"

    try:
        str_doc= db[doc_id][2]
    except:
        return {}

    document = ast.literal_eval(str_doc)
    log.debug("Document fetched is: " + str(document))
    return document

str_value='{"external_dns_status": "false", "ping_status": "rtt min/avg/max/mdev = 0.635/0.635/0.635/0.000 ms"}'
value = ast.literal_eval(str_value)
print value