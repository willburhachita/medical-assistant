from rest_framework.serializers import ModelSerializer
from user.models import User


class UserLookupSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'wallet_address', 'full_name', 'email_address',)


class UserGetSerializer(ModelSerializer):

    class Meta:
        model = User
        exclude = ("wallet_address", "id", "groups", "user_permissions", )


class UserPatchSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ("wallet_address", "id", "groups", "user_permissions", "is_superuser",)


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ("full_name", "password","is_superuser", "is_staff", )
