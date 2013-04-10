import shelve
from server import constants
from server.logger import logger


log = logger("Nodelist")

def write_node_list(nodes):

    s = shelve.open('node_list_shelf.db', writeback = True)
    try:
        log.info("writing node list to file" + str(nodes))
        s['node_list']= nodes
    finally:
        s.close()

    #cache this list::
    constants.nodes = get_node_list()

def get_node_list():

    nodes=[]
    s = shelve.open('node_list_shelf.db', writeback = True)
    try:
        log.debug("Getting node list from file")
        if('node_list' in s):
            nodes = s['node_list']

    finally:
        s.close()

    return nodes