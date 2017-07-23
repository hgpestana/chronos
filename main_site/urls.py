"""timesheet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from django.contrib import admin

handler404 = 'apps.core.views.error404'
handler500 = 'apps.core.views.error500'


urlpatterns = [
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^account/', include('apps.account.urls', namespace='account')),
    url(r'^client/', include('apps.client.urls', namespace='client')),
    url(r'^project/', include('apps.project.urls', namespace='project')),
    url(r'^entry/', include('apps.entry.urls', namespace='entry')),
    url(r'^login/', include('apps.login.urls', namespace='login')),
    url(r'^task/', include('apps.task.urls', namespace='task')),
    url(r'^', include('apps.core.urls', namespace='index')),
]

