from django.contrib.auth import authenticate, get_user_model, login
from rest_framework import serializers

from social_network.utils.authutils import get_tokens

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for fetching User details.
    """

    class Meta:
        model = User
        fields = ["id", "email", "name"]


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """

    class Meta:
        model = User
        fields = ["email", "name", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def to_internal_value(self, data):
        data["email"] = data.get("email") and data["email"].lower()
        return super().to_internal_value(data)

    def to_representation(self, instance):
        """
        Custom representation of the user instance with tokens.
        """
        return {"user": UserSerializer(instance).data, **get_tokens(instance)}


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def to_internal_value(self, data):
        data["email"] = data.get("email") and data["email"].lower()
        return super().to_internal_value(data)

    def create(self, validated_data):
        """
        Authenticate and log in the user with email and password.
        """
        email = validated_data.get("email")
        password = validated_data.get("password")
        user = authenticate(email=email, password=password)
        if user:
            login(self.context["request"], user)
            return user
        raise serializers.ValidationError({"error": "Invalid credentials"})

    def to_representation(self, instance):
        """
        Custom representation of the user instance with tokens.
        """
        return {"user": UserSerializer(instance).data, **get_tokens(instance)}
