from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.EntryIndexView.as_view(), name='index'),
    url(r'^add/$', views.EntryAddView.as_view(), name='add'),
    url(r'^view/(?P<pk>[0-9]+)/$', views.EntryDetailView.as_view(), name='view'),
    url(r'^edit/(?P<pk>[0-9]+)/$', views.EntryEditView.as_view(), name='edit'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.EntryDeleteView.as_view(), name='delete'),
    url(r'^(?P<result>.*)$', views.EntryIndexView.as_view(), name='index'),
]