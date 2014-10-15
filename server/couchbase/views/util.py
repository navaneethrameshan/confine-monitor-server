def get_sum_count(view_stats):
    total_sum = 0
    total_count = 0
    node_id_map = {}

    for view in view_stats:
        document = view['value']
        key = view['key']
        print "Key: " + str(key)
        node_id = str(key[:1]).strip('[]')
        if node_id_map.has_key(node_id):
            total_sum+= document['sum']
            total_count+= document['count']
            node_id_map.update({node_id:{'total_sum':total_sum, 'total_count': total_count}})
        else:
            total_sum = document['sum']
            total_count= document['count']
            node_id_map.update({node_id:{'total_sum':total_sum, 'total_count': total_count}})

    return node_id_map
