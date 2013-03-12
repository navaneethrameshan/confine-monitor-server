from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'web.views.index'),
    url(r'^loadavg/([A-Za-z]*-\d*)$', 'web.views.load_avg_1min'), # currently accept "word - number"
    url(r'^freemem/([A-Za-z]*-\d*)$', 'web.views.free_mem'), # currently accept "word - number"
    url(r'^uptime/([A-Za-z]*-\d*)$', 'web.views.uptime'), # currently accept "word - number"
    url(r'^cpuusage/([A-Za-z]*-\d*)$', 'web.views.cpu_usage'), # currently accept "word - number"
    url(r'^datasent/([A-Za-z]*-\d*)$', 'web.views.data_sent'), # currently accept "word - number"
    url(r'^datareceived/([A-Za-z]*-\d*)$', 'web.views.data_received'), # currently accept "word - number"
    url(r'^nodeslivers/(.{2,})$', 'web.views.node_slivers'), # Accept atleast 2 characters
    url(r'^slice/([A-Za-z]*-\d*)$', 'web.views.slice_info'), # currently accept "word - number"
    url(r'^slivercpuusage/(.{2,})$', 'web.views.sliver_cpu_usage'), # Accept atleast 2 characters
    url(r'^nodenetwork/(.{2,})$', 'web.views.node_network'), # Accept atleast 2 characters
    # url(r'^web/', include('web.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
