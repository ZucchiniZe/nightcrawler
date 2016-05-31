from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^comics/$', views.AllTitleView.as_view(), name='listing'),
    url(r'^synced/$', views.SyncedView.as_view(), name='synced'),
    url(r'^comic/(?P<pk>[0-9]+)/$', views.ComicView.as_view(), name='comic'),
    url(r'^issue/(?P<pk>[0-9]+)/$', views.IssueView.as_view(), name='issue'),
    url(r'^creator/(?P<pk>[0-9]+)/$', views.CreatorView.as_view(), name='creator'),
    url(r'^refresh/comics/$', views.refresh_comics, name='refresh_comics'),
    url(r'^refresh/issues/(?P<pk>[0-9]+)/$', views.refresh_issues, name='refresh_issues'),
]