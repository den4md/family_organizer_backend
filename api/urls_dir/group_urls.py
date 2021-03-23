from django.urls import path

from api.views_dir.group_views import group_view, group_members_view, group_join_view, group_leave_view, group_list_view

urlpatterns = [
    path('group', group_view.GroupView.as_view),
    path('group/members', group_members_view.GroupMembersView.as_view),
    path('group/join', group_join_view.GroupJoinView.as_view),
    path('group/leave', group_leave_view.GroupLeaveView.as_view),
    path('group/list', group_list_view.GroupListView.as_view),
]
