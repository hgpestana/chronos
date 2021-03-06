from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.AccountIndexView.as_view(), name='index'),
	url(r'^add/$', views.AccountAddView.as_view(), name='add'),
	url(r'^view/(?P<pk>[0-9]+)/$', views.AccountDetailView.as_view(), name='view'),
	url(r'^edit/(?P<pk>[0-9]+)/$', views.AccountEditView.as_view(), name='edit'),
	url(r'^delete/(?P<pk>[0-9]+)/$', views.AccountDeleteView.as_view(), name='delete'),
	url(r'^(?P<result>.*)$', views.AccountIndexView.as_view(), name='index'),
]
