from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mockstocks.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Index of site
    url(r'^dashboard/$', 'game.views.dashboard', name='dashboard'),

    # Transaction history
    url(r'^history/$', 'game.views.history', name='transaction history'),

    # All companies
    url(r'^companies/$', 'game.views.companies', name='all companies'),

    # Sell Shares
    url(r'^sell/$', 'game.views.sell', name='sell shares'),

    # Buy Shares
    url(r'^buy/$', 'game.views.buy', name='buy shares'),

)
