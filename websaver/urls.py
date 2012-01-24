from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  url(r'^signup/$', 'wbesaver.users.views.registration.register'),
  url(r'^$', 'websaver.users.views.registration.register'),
  url(r'^account_activation\?user_id=(?P<user_id>[0-9]+)&activation_key=(?P<activation_key>[0-9a-zA-Z]+)$',
      'websaver.users.views.registration.activate_registration'),
    # Examples:
    # url(r'^$', 'websaver.views.home', name='home'),
    # url(r'^websaver/', include('websaver.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()