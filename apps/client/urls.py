from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.ClientIndexView.as_view(), name='index'),
	url(r'^add/$', views.ClientAddView.as_view(), name='add'),
	url(r'^view/(?P<pk>[0-9]+)/$', views.ClientDetailView.as_view(), name='view'),
	url(r'^edit/(?P<pk>[0-9]+)/$', views.ClientEditView.as_view(), name='edit'),
	url(r'^delete/(?P<pk>[0-9]+)/$', views.ClientDeleteView.as_view(), name='delete'),
	url(r'^(?P<result>.*)$', views.ClientIndexView.as_view(), name='index'),
]
