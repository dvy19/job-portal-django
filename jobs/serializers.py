
from rest_framework import serializers

from .models import Blog, Job, JobApplication

class BlogSerializer(serializers.ModelSerializer):

    recruiter = serializers.StringRelatedField(source='user', read_only=True)

    class Meta:
        model = Blog
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']

# 🔹 Job Serializer
class JobSerializer(serializers.ModelSerializer):
    recruiter = serializers.StringRelatedField(read_only=True)

    skills = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )

    skill_names = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['id', 'created_at','user', 'updated_at']

    def create(self, validated_data):
        skills_data = validated_data.pop('skills', [])

        job = Job.objects.create(**validated_data)

        for skill_name in skills_data:
            skill, _ = "accounts.Skill".objects.get_or_create(name=skill_name)
            job.skills.add(skill)

        return job

    def update(self, instance, validated_data):
        skills_data = validated_data.pop('skills', None)

        # Update normal fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update skills if provided
        if skills_data is not None:
            instance.skills.clear()
            for skill_name in skills_data:
                skill, _ = "accounts.Skill".objects.get_or_create(name=skill_name)
                instance.skills.add(skill)

        return instance
    

class JobApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ['applicant', 'status', 'applied_at']


