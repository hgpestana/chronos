from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.CoreIndexView.as_view(), name='index'),
]
