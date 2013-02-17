def create_view (db, doc_name, map_function, view_name ):
# check if there are entries for same document_id

    map_load_avg =  map_function

    design = { 'views': {
        view_name: {
            'map':map_load_avg
        }
    } }

    document_id = '_design/'+ doc_name

    db[document_id] = design
    #   print str(db['_design/loadavglist'])

