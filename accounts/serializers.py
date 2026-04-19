from rest_framework import serializers
from .models import CustomUser, RecruiterProfile, Skill
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
    

  