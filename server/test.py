from server.couchbase import documentparser

def rename_sliver(seq_value, name):
    slivers = documentparser.get_value(seq_value, 'slivers')

    for container in slivers:
        sliver= slivers[container]
        sliver_name = documentparser.get_value(sliver, 'sliver_name')
        sliver_slice_name = documentparser.get_value(sliver, 'sliver_slice_name')
        ##Update Sliver name##
        sliver_name = str(sliver_slice_name) + name
        seq_value['slivers'][container]['sliver_name'] = sliver_name
