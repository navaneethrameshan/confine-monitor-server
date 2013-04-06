from server.couchbase import main   
import os

path= os.path.join(os.path.dirname(__file__), 'node_list_shelf.db')
if(os.path.exists(path)):
    os.remove(path)
main.main()
