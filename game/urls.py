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

    # Buy and offer
    url(r'^buyoffer/(?P<offer_id>\d+)/$', 'game.views.buyoffer', name='accept an offer'),

    # Remove an offer
	url(r'^remove/(?P<offer_id>\d+)/$', 'game.views.remove_offer', name='remove offer'),

	# Gets max shares of user of particular company
    url(r'^getmax/$', 'game.views.max_shares', name='get max shares'),

    # Gets currprice and netchange of all companies
    url(r'^getprices/$', 'game.views.get_curr_prices', name='get curr prices'),

    # Get currprice of a company
    url(r'^getcurprice/$', 'game.views.get_curr_price', name='get curr price'),

    # Transaction history
    url(r'^history/(?P<company_id>\d+)/$', 'game.views.history', name='transaction history'),

    # Gets currprice and netchange of all companies
    url(r'^getinfo/$', 'game.views.getinfo', name='get company info'),

    # Initshare buy function
    url(r'^initbuy/$', 'game.views.initbuy', name='initshare buy'),

)
