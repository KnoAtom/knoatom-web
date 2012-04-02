from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/?$', 'web.views.account.login', name='login'),
    url(r'^logout/?$', 'web.views.account.logout', name='logout'),
    url(r'^register/?$', 'web.views.account.register', name='register'),
    url(r'^forgot_password/?$', 'web.views.account.forgot_password', name='forgot_password'),

    url(r'^ajax/vote/(\d+)/(\d+)/?$', 'web.views.ajax.vote', name='vote'),

    url(r'^submit/?$', 'web.views.submission.index', name='submit'),

    url(r'^category/(\d+)/?$', 'web.views.home.category', name='category'),
    url(r'^$', 'web.views.home.index', name='home'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^mu-25b8a55c-a9fee579-723dcc44-9782bfc2$', 'web.views.blitz.index'),
)
