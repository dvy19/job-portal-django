from rest_framework import serializers
from .models import CustomUser, RecruiterProfile
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import JobSeekerProfile

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
    

class LoginSerializer(serializers.Serializer):

    email    = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        # Generate tokens
        refresh = RefreshToken.for_user(user)

        return {
            "user": user,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "role": user.role
        }
    



class RecruiterProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=RecruiterProfile
        fields='__all__'
        read_only_fields = ['user'] 
        

    
    def create(self,validated_data):
        profile=RecruiterProfile.objects.create(**validated_data)
        return profile



class JobSeekerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobSeekerProfile
        fields = '__all__'
        read_only_fields = ['user']  # user will be set from the view, not the request data

    def create(self, validated_data):
        profile = JobSeekerProfile.objects.create(**validated_data)
        return profile

    

  