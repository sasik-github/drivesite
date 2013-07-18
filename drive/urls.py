from django.conf.urls import patterns, include, url

from drive import views

urlpatterns = patterns('',
	url(r'^$', views.index, name = 'index'),
	# drive/list?code=4/jiHuLZh4sHngRU3YLgGsJ9e8VI88.QsGkDh1TU68UsNf4jSVKMpY4aqvafwI
	# url(r'^list?code=4/(?P<code>\w+)$', views.list, name = 'list'),
	url(r'^list', views.list, name = 'list'),
	# url(r'^list?code=4/(P<code>\d+)/$', views.list, name = 'list'),

	)
