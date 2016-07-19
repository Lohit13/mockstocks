from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mockstocks.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # Index of site
    url(r'^$', 'mockstocks.views.index', name='home'),

    # Rules and instructions
    url(r'^howto/$', 'mockstocks.views.howto', name='how to play'),

    # Register new user
    url(r'^register/$', 'mockstocks.views.register', name='register'),

    # Leaderboard
    url(r'^leaderboard/$', 'mockstocks.views.leaderboard', name='leaderboard'),

    # Logs the user in
    url(r'^login/$', 'mockstocks.views.sign_in', name='login'),

    # Logs the user out
    url(r'^logout/$', 'mockstocks.views.logout', name='logout'),

    # Game urls
    (r'^', include('game.urls')),

)
