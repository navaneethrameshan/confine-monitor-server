from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'web.views.index'),
    url(r'^(visualize/.{0,})$', 'web.views.node_info_treemap'),
    url(r'^(load_avg_1min/.{2,})$', 'web.views.node_info_timeline'),
    url(r'^(memory_percent_used/.{2,})$', 'web.views.node_info_timeline'),
    url(r'^(uptime/.{2,})$', 'web.views.node_info_timeline'),
    url(r'^(total_cpu_usage/.{2,})$', 'web.views.node_info_timeline'),
    url(r'^(network_total_bytes_sent_last_sec/.{2,})$', 'web.views.node_info_timeline'),
    url(r'^(network_total_bytes_received_last_sec/.{2,})$', 'web.views.node_info_timeline'),
    url(r'^nodeslivers/(.{2,})$', 'web.views.node_slivers'),
    url(r'^slice/(.{2,})$', 'web.views.slice_info'),
    url(r'^slivercpuusage/(.{2,})$', 'web.views.sliver_cpu_usage'),
    url(r'^slivermemoryusage/(.{2,})$', 'web.views.sliver_memory_usage'),

    url(r'^async_aggr/(.{2,})$', 'web.views.async_aggr_node_attribute'),
    url(r'^async_aggr_json/(.{2,})$', 'web.views.async_aggr_node_attribute_json'),
    url(r'^async_aggr_set/(.{2,})$', 'web.views.async_aggr_set_node_attribute'),
    url(r'^async_aggr_set_json/(.{2,})$', 'web.views.async_aggr_set_node_attribute_json'),

    url(r'^async/(.{2,})$', 'web.views.async_node_attribute'),
    url(r'^async_json/(.{2,})$', 'web.views.async_node_attribute_json'),


    url(r'^pingstatus/(.{2,})$', 'web.views.node_ping'),


    url(r'^(network/.{2,})$', 'web.views.node_info_set_timeline'),
    url(r'^(disk/.{2,})$', 'web.views.node_info_set_timeline'),
    url(r'^(memory/.{2,})$', 'web.views.node_info_set_timeline'),
    url(r'^(networktrace/.{0,})$', 'web.views.network_trace'),
    url(r'^(internodetrace/.{2,})$', 'web.views.inter_node_trace'),
    url(r'^(allinternodetrace/.{0,})$', 'web.views.all_inter_node_trace'),
    url(r'^(allinternodematrix/.{0,})$', 'web.views.all_inter_node_matrix'),


    # url(r'^web/', include('web.foo.urls')),
    #url(r'^slice/([A-Za-z]*-\d*)$', 'web.views.slice_info'), # currently accept "word - number"

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
