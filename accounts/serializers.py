from rest_framework import serializers
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):

    # write_only = password will never be sent back in response
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model  = CustomUser
        fields = ["email", "password", "role"]

    def create(self, validated_data):
        # Use our custom manager to create the user
        user = CustomUser.objects.create_user(
            email    = validated_data["email"],
            password = validated_data["password"],
            role     = validated_data["role"],
        )
        return user