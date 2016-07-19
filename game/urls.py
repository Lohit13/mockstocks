from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mockstocks.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Index of site
    url(r'^dashboard/$', 'game.views.dashboard', name='dashboard'),

)
