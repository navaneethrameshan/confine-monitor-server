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

    cherrypy.server.socket_host = '84.88.85.24'
    cherrypy.engine.start()


if __name__ =='__main__':
    path= os.path.join(os.path.dirname(__file__), 'node_list_shelf.db')
    if(os.path.exists(path)):
        os.remove(path)

    launch_memory_usage_server()
    main.main()
