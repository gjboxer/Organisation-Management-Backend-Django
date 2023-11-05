from rest_framework import serializers
from .models import Organization, Invitation, Task
from django.contrib.auth.models import User


class JoinOrganizationSerializer(serializers.Serializer):
    organization = serializers.ChoiceField(
        choices=[(org.name, org.name) for org in Organization.objects.all()],
        write_only=True,
    )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'name', 'description')


class InvitationSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    recipient = serializers.StringRelatedField()
    organization = serializers.StringRelatedField()

    class Meta:
        model = Invitation
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    assigned_users = serializers.StringRelatedField(many=True)
    organization = serializers.StringRelatedField()

    class Meta:
        model = Task
        fields = '__all__'


class InvitationCreateSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)
    recipient = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all(), required=True)

    class Meta:
        model = Invitation
        fields = ['sender', 'recipient', 'organization']
