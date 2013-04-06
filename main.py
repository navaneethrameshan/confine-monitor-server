from server.couchbase import main   
import os

def launch_memory_usage_server(port = 8088):
    import cherrypy
    import dowser
 
    cherrypy.tree.mount(dowser.Root())
    cherrypy.config.update({
        'environment': 'embedded',
        'server.socket_port': port
    })
   
    cherrypy.server.socket_host = '147.83.35.241'
    cherrypy.engine.start()

path= os.path.join(os.path.dirname(__file__), 'node_list_shelf.db')
if(os.path.exists(path)):
    os.remove(path)

launch_memory_usage_server()
main.main()
