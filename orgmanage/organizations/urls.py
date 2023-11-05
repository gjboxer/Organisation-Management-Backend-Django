from django.urls import path
from . import views
from .views import UserInvitationsListView

urlpatterns = [
    path('organizations/', views.OrganizationList.as_view(),
         name='organization-list'),
    path('organizations/<int:pk>/', views.OrganizationDetail.as_view(),
         name='organization-detail'),
    path('current-user-organization/', views.CurrentUserOrganizationView.as_view(),
         name='current-user-organization'),
    path('invitations/', views.InvitationCreateView.as_view(),
         name='invitation-create'),
    path('invitations/<int:pk>/accept-reject/',
         views.AcceptRejectInvitationView.as_view(), name='accept-reject-invitation'),
    path('user-invitations/', UserInvitationsListView.as_view(),
         name='user-invitations-list'),
    path('join-organization/', views.JoinOrganizationView.as_view(),
         name='join-organization'),
    path('tasks/', views.UserTasksListView.as_view(), name='user-tasks-list'),

]
