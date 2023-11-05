from .models import Organization, Membership, Task, Invitation
from rest_framework import generics
from .serializers import TaskSerializer, OrganizationSerializer, InvitationSerializer, InvitationCreateSerializer, UserSerializer, JoinOrganizationSerializer
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

class CurrentUserOrganizationView(generics.ListAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]
    queryset = Organization.objects.all()
    lookup_field = None
    lookup_url_kwarg = None

    def get_queryset(self):
        return self.request.user.organizations.all()

class JoinOrganizationView(APIView):
    serializer_class = JoinOrganizationSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = JoinOrganizationSerializer(data=request.data)

        if serializer.is_valid():
            organization_name = serializer.validated_data.get('organization')
            organization = Organization.objects.filter(
                name=organization_name).first()

            if not organization:
                return Response({"detail": "Organization not found."}, status=status.HTTP_404_NOT_FOUND)

            # Check if the user is already a member of the organization
            if organization.members.filter(id=request.user.id).exists():
                return Response({"detail": "You are already a member of this organization."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the user is already a member of the organization
            if Membership.objects.filter(user=request.user, organization=organization).exists():
                return Response({"detail": "You are already a member of this organization."}, status=status.HTTP_400_BAD_REQUEST)

            # Create a membership for the user in the organization
            Membership.objects.create(
                user=request.user, organization=organization)
            return Response({"detail": "You have successfully joined the organization."}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserInvitationsListView(generics.ListAPIView):
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter invitations where the current user is the recipient.
        return Invitation.objects.filter(recipient=self.request.user)


class OrganizationList(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class OrganizationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class InvitationCreateView(generics.CreateAPIView):
    queryset = Invitation.objects.all()
    serializer_class = InvitationCreateSerializer

    def perform_create(self, serializer):
        organization_name = serializer.validated_data.get('organization')
        recipient_username = serializer.validated_data.get('recipient')
        organization = Organization.objects.filter(
            name=organization_name).first()

        if not organization:
            return Response({"detail": "Organization not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has permission to invite to this organization
        if not organization.members.filter(id=self.request.user.id).exists():
            return Response({"detail": "You do not have permission to invite members to this organization."}, status=status.HTTP_403_FORBIDDEN)

        recipient = User.objects.filter(username=recipient_username).first()
        if not recipient:
            return Response({"detail": "Recipient not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the recipient is already a member of the organization
        if organization.members.filter(id=recipient.id).exists():
            return Response({"detail": "The recipient is already a member of this organization."}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(sender=self.request.user, status='pending')
        return Response({"detail": "Invitation sent."}, status=status.HTTP_201_CREATED)


class AcceptRejectInvitationView(generics.RetrieveUpdateAPIView):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        invitation = self.get_object()

        if invitation.recipient == request.user:
            if invitation.status == 'pending':
                # Accept the invitation
                invitation.status = 'accepted'
                invitation.save()

                # Create a membership for the user in the organization
                Membership.objects.create(
                    user=request.user, organization=invitation.organization)

                return Response({'detail': 'Invitation accepted and user joined the organization.'})
            elif invitation.status == 'accepted':
                return Response({'detail': 'Invitation has already been accepted'})
            elif invitation.status == 'rejected':
                return Response({'detail': 'Invitation has already been rejected'})
        else:
            return Response({'detail': 'You do not have permission to update this invitation.'}, status=403)


class UserTasksListView(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(assigned_users=self.request.user)
