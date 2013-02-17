from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'web.views.index'),
    url(r'^lol/$', 'web.views.hello'),
    url(r'^gtest/$', 'web.views.gtest'),
    url(r'^loadavg/(\d+.*)$', 'web.views.load_avg_1min'), # currently accept only ip addresses as names
    url(r'^freemem/(\d+.*)$', 'web.views.freemem'), # currently accept only ip addresses as names
    url(r'^uptime/(\d+.*)$', 'web.views.uptime'), # currently accept only ip addresses as names
    url(r'^cpuusage/(\d+.*)$', 'web.views.cpu_usage'), # currently accept only ip addresses as names
    # url(r'^web/', include('web.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
