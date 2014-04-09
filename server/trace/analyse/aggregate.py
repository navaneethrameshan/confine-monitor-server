
#get information from all the RD's
class Paths(object):

    def __init__(self):
        self.paths= [] #list of paths stored as probe objects for all the RDs. List of list [[node1probe1,node1probe2,..],[node2probe1,node3probe2,.],...[]]

    def add_path(self, path):
        self.paths.append(path)

    def get_paths(self):
        return self.paths



class Analyse(object):

    def __init__(self):
        self.representation = {} # key = router/node, value = parent
        self.nodes = {}

    def represent(self, pathsobject):
        if isinstance(pathsobject,Paths):
            pathlist = pathsobject.get_paths()
            for path in pathlist:
                firstrun = True
                for probe in path:
                    if probe.has_key("Name"):
                        if firstrun:
                            parent = probe["Name"]
                            self.nodes[probe["Name"]]= 1 ## Value 1 indicates that the node is an RD
                            firstrun = False
                        else:
                            #print "Adding to dict- Key: " +str(probe["Name"]) +"  Value: "+str(parent)
                            self.__add_to_dict(probe["Name"],parent)
                            parent = probe["Name"]
                            self.nodes[probe["Name"]]= 0 ## Value 0 indicates not an RD

        else:
            print "[ERROR] Not an Instance of Paths."

    def __add_to_dict(self, k, v):
        if self.representation.has_key(k):
            present = False
            value_list = self.representation[k]
            for val in value_list:
                if val == v:
                    present = True
            if not present:
                value_list.append(v)

        else:
            self.representation[k] = [v]

       # print str(self.representation)

    def get_representation(self):
        return self.representation

    def get_nodes(self):
        return  self.nodes