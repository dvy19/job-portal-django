import os
from dotenv import load_dotenv
import token

from rest_framework import serializers
from .models import CustomUser, RecruiterProfile, Skill
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import JobSeekerProfile

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.password_validation import validate_password

#Load environment variables from .env file
load_dotenv()


class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        uid = attrs.get("uid")
        token = attrs.get("token")
        password = attrs.get("password")

        # Decode UID
        try:
            user_id = urlsafe_base64_decode(uid).decode()
            user = CustomUser.objects.get(id=user_id)
        except:
            raise serializers.ValidationError("Invalid user")

        # Validate token
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("Invalid or expired token")

        # Validate password (Django built-in validators)
        validate_password(password, user)

        # Store user for save()
        self.user = user
        return attrs

    def save(self):
        password = self.validated_data["password"]

        self.user.set_password(password)
        self.user.save()

        return self.user
    
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        # We don't raise error if user doesn't exist (security)
        self.user = CustomUser.objects.filter(email=value).first()
        return value

    def save(self):
        if not self.user:
            return  # silently ignore

        # Generate token + uid
        token = PasswordResetTokenGenerator().make_token(self.user)
        uid = urlsafe_base64_encode(force_bytes(self.user.id))
        
        print("UID:", uid)
        print("TOKEN:", token)
        # Reset link (frontend URL)
        reset_link = f"https://job-portal-django-1-rc3u.onrender.com/api/jobs/reset-password/{uid}/{token}/"

        print("RESET LINK:", reset_link)

        # Send email
        send_mail(
            subject="Reset Your Password",
            message=f"Click the link to reset your password:\n{reset_link}",
            from_email=os.getenv("EMAIL_HOST_USER"),
            recipient_list=[self.user.email],
        )

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
        

    
  

class JobSeekerProfileSerializer(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Skill.objects.all()
    )

    class Meta:
        model = JobSeekerProfile
        fields = '__all__'
        read_only_fields = ['user']
        

    def create(self, validated_data):
        skills = validated_data.pop('skills', [])  # extract skills
        profile = JobSeekerProfile.objects.create(**validated_data)
        profile.skills.set(skills)  # assign many-to-many
        return profile
    
    def update(self, instance, validated_data):
        skills = validated_data.pop('skills', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        if skills is not None:
            instance.skills.set(skills)

        return instance

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']
        read_only_fields = ['id']
    

  