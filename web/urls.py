from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'web.views.index'),
    url(r'^loadavg/([A-Za-z]*-\d*)$', 'web.views.load_avg_1min'), # currently accept "word - number"
    url(r'^freemem/([A-Za-z]*-\d*)$', 'web.views.freemem'), # currently accept "word - number"
    url(r'^uptime/([A-Za-z]*-\d*)$', 'web.views.uptime'), # currently accept "word - number"
    url(r'^cpuusage/([A-Za-z]*-\d*)$', 'web.views.cpu_usage'), # currently accept "word - number"
    # url(r'^web/', include('web.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
