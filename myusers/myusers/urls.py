from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myusers.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # create a url for each of the main CRUD functions
    url(r'^$', views.HomepageView.as_view(), name='home'),
    url(r'^myusers/retrieve$', views.MyUserListView.as_view(), name='list'),
    url(r'^myusers/create/$', views.MyUserCreateView.as_view(), name='create'),
    url(r'^myusers/(?P<pk>\d+)/retrieve$', views.MyUserDetailView.as_view(), name='detail'),
    url(r'^myusers/(?P<pk>\d+)/update/$', views.MyUserUpdateView.as_view(), name='update'),
    url(r'^myusers/(?P<pk>\d+)/destroy/$', views.MyUserDeleteView.as_view(), name='destroy'),
    url(r'^admin/', include(admin.site.urls))
)
