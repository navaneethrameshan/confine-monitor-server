class Generate(object):

    def __init__(self, representation):
        if isinstance(representation, dict):
            self.generated_nodes = []
            self.generated_edges=[]
        else:
            print "[Error]: Wrong Input to generate JSON. Make sure the input is a dictionary"

    def generate_json(self, representation):
        for key,values in representation.items():
            self.generated_nodes.append({'id':str(key), 'label':str(key)})
            for value in values:
                self.generated_edges.append({'from':str(key),'to':str(value)})
       # print str(self.generated_nodes)
       # print str(self.generated_edges)
        return {'nodes':self.generated_nodes, 'edges': self.generated_edges}