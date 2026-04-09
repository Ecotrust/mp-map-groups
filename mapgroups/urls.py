"""URL configuration for the mapgroups app."""
from django.urls import path, re_path

from mapgroups.views import (
    MapGroupDetailView, MapGroupCreate, MapGroupListView,
    JoinMapGroupActionView, RequestJoinMapGroupActionView,
    MapGroupEditView, MapGroupPreferencesView, LeaveMapGroupActionView,
    DeleteMapGroupActionView, RemoveMapGroupImageActionView,
    ApproveMapGroupActionView, DenyMapGroupActionView,
    PromoteMapGroupMemberActionView, RemoveMapGroupMemberActionView,
    DemoteMapGroupMemberActionView,
)

app_name = 'mapgroups'

urlpatterns = [
    # Map group urls look something like:
    #   midatlanticoceans.org/g/49/swiftly-sinking-sailfish
    # but
    #   midatlanticoceans.org/g/49
    # will also work

    re_path(r'^$', MapGroupListView.as_view(), name='list'),
    re_path(r'^create$', MapGroupCreate.as_view(), name='create'),
    re_path(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/edit$',
        MapGroupEditView.as_view(), name='edit'),
    re_path(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/edit/remove-image$',
        RemoveMapGroupImageActionView.as_view(), name='remove-image'),
    re_path(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/$',
        MapGroupDetailView.as_view(), name='detail'),
    re_path(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/preferences/?$',
        MapGroupPreferencesView.as_view(), name='preferences'),
    re_path(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/join$',
        JoinMapGroupActionView.as_view(), name='join'),
    re_path(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/leave$',
        LeaveMapGroupActionView.as_view(), name='leave'),
    re_path(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/delete$',
        DeleteMapGroupActionView.as_view(), name='delete'),
    re_path(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/join$',
        RequestJoinMapGroupActionView.as_view(), name='request-join'),
    re_path(r'^(?P<pk>\d+)/approve$',
        ApproveMapGroupActionView.as_view(), name='request-approve'),
    re_path(r'^(?P<pk>\d+)/deny$',
        DenyMapGroupActionView.as_view(), name='request-deny'),
    re_path(r'^(?P<pk>\d+)/promote$',
        PromoteMapGroupMemberActionView.as_view(), name='promote-member'),
    re_path(r'^(?P<pk>\d+)/demote$',
        DemoteMapGroupMemberActionView.as_view(), name='demote-member'),
    re_path(r'^(?P<pk>\d+)/remove$',
        RemoveMapGroupMemberActionView.as_view(), name='remove-member'),
]

def urls(namespace='mapgroups'):
    """Returns a 3-tuple for use with include().

    The including module or project can refer to urls as namespace:urlname,
    internally, they are referred to as app_name:urlname.
    """
    return (urlpatterns, 'mapgroups', namespace)
