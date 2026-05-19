from django.contrib.auth.models import User
from rest_framework import serializers

from profiles.models import Profile


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already taken.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value

    def create(self, validated_data):
        bio = validated_data.pop('bio', '')
        phone = validated_data.pop('phone', '')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        Profile.objects.create(
            user=user,
            bio=bio,
            phone=phone,
            created_by=user,
            updated_by=user,
        )
        return {
            'user_id': user.id,
            'profile_id': user.profile.id,
            'username': user.username,
            'email': user.email,
        }
