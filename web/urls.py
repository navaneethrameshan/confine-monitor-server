from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'web.views.index'),
    url(r'^(visualize/.{2,})$', 'web.views.node_info_treemap'),
    url(r'^(load_avg_1min/.{2,})$', 'web.views.node_info_timeline'),
    url(r'^(free_memory/.{2,})$', 'web.views.node_info_timeline'),
    url(r'^(uptime/.{2,})$', 'web.views.node_info_timeline'),
    url(r'^(total_cpu_usage/.{2,})$', 'web.views.node_info_timeline'),
    url(r'^(network_total_bytes_sent_last_sec/.{2,})$', 'web.views.node_info_timeline'),
    url(r'^(network_total_bytes_received_last_sec/.{2,})$', 'web.views.node_info_timeline'),
    url(r'^nodeslivers/(.{2,})$', 'web.views.node_slivers'),
    url(r'^slice/(.{2,})$', 'web.views.slice_info'),
    url(r'^slivercpuusage/(.{2,})$', 'web.views.sliver_cpu_usage'),
    url(r'^slivermemoryusage/(.{2,})$', 'web.views.sliver_memory_usage'),


    url(r'^pingstatus/(.{2,})$', 'web.views.node_ping'),


    url(r'^(network/.{2,})$', 'web.views.node_info_set_timeline'),
    url(r'^(disk/.{2,})$', 'web.views.node_info_set_timeline'),
    url(r'^(memory/.{2,})$', 'web.views.node_info_set_timeline'),

    # url(r'^web/', include('web.foo.urls')),
    #url(r'^slice/([A-Za-z]*-\d*)$', 'web.views.slice_info'), # currently accept "word - number"

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
