
from rest_framework import serializers

from .models import Blog, Job, JobApplication
from accounts.models import Skill

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

    skill_names = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'user', 'updated_at']

    def get_skill_names(self, obj):
        return [skill.name for skill in obj.skills.all()]

    def create(self, validated_data):
        skills_data = validated_data.pop('skills', [])

        job = Job.objects.create(**validated_data)

        for skill_name in skills_data:
            skill, _ = Skill.objects.get_or_create(name=skill_name)
            job.skills.add(skill)

        return job

    def update(self, instance, validated_data):
        skills_data = validated_data.pop('skills', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if skills_data is not None:
            instance.skills.clear()
            for skill_name in skills_data:
                skill, _ = Skill.objects.get_or_create(name=skill_name)
                instance.skills.add(skill)

        return instance
    

class JobApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ['applicant', 'status', 'applied_at']


