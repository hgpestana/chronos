from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.TaskIndexView.as_view(), name='index'),
    url(r'^add/$', views.TaskAddView.as_view(), name='add'),
    url(r'^view/(?P<pk>[0-9]+)/$', views.TaskDetailView.as_view(), name='view'),
    url(r'^edit/(?P<pk>[0-9]+)/$', views.TaskEditView.as_view(), name='edit'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.TaskDeleteView.as_view(), name='delete'),
    url(r'^(?P<result>.*)$', views.TaskIndexView.as_view(), name='index'),
]