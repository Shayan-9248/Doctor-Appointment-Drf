# Core django imports import
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
from django.contrib.auth import get_user_model

# Third-party import
from rest_framework import serializers

User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(
    #     view_name="api_account:retrieve", lookup_field="pk"
    # )

    class Meta:
        model = User
        fields = (
            # "url",
            "username",
            "email",
            "id",
        )


class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "phone_number",
            "first_name",
            "last_name",
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "phone_number",
            "first_name",
            "last_name",
        )
        extra_kwargs = {"username": {"read_only": True}, "email": {"read_only": True}}


class CreateNewUserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """

    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def validate_username(self, value):
        qs = User.objects.filter(username__icontains=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("This username has already exists")
        return value

    def validate_email(self, value):
        qs = User.objects.filter(email__icontains=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("This email address has already exists")
        return value

    def create(self, validated_data):
        username = validated_data.get("username")
        email = validated_data.get("email")
        password = validated_data.get("password")
        user_obj = User(
            username=username,
            email=email,
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=70)
    token = serializers.CharField(max_length=300, write_only=True)

    class Meta:
        model = User
        fields = ("username", "token", "password")

        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password")
        if not username:
            raise ValidationError("Enter your username")

        user = User.objects.filter(Q(username=username)).distinct()
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("Username not found")

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Password is incorrect")
            data["token"] = "some random token"
        return data


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value
