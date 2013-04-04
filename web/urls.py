from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'web.views.index'),
    url(r'^loadavg/(.{2,})$', 'web.views.load_avg_1min'),
    url(r'^freemem/(.{2,})$', 'web.views.free_mem'),
    url(r'^uptime/(.{2,})$', 'web.views.uptime'),
    url(r'^cpuusage/(.{2,})$', 'web.views.cpu_usage'),
    url(r'^datasent/(.{2,})$', 'web.views.data_sent'),
    url(r'^datareceived/(.{2,})$', 'web.views.data_received'),
    url(r'^nodeslivers/(.{2,})$', 'web.views.node_slivers'),
    url(r'^slice/(.{2,})$', 'web.views.slice_info'),
    url(r'^slivercpuusage/(.{2,})$', 'web.views.sliver_cpu_usage'),
    url(r'^slivermemoryusage/(.{2,})$', 'web.views.sliver_memory_usage'),
    url(r'^nodenetwork/(.{2,})$', 'web.views.node_network'),
    url(r'^nodedisk/(.{2,})$', 'web.views.node_disk'),

    url(r'^network/(.{2,})$', 'web.views.network_timeline'), # currently accept "word - number"
    url(r'^disk/(.{2,})$', 'web.views.disk_timeline'), # currently accept "word - number"

    # url(r'^web/', include('web.foo.urls')),
    #url(r'^slice/([A-Za-z]*-\d*)$', 'web.views.slice_info'), # currently accept "word - number"

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
