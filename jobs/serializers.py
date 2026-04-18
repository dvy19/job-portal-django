
from rest_framework import serializers

from .models import Blog, Job

class BlogSerializer(serializers.ModelSerializer):

    recruiter = serializers.StringRelatedField(source='user', read_only=True)

    class Meta:
        model = Blog
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']

# 🔹 Job Serializer
class JobSerializer(serializers.ModelSerializer):
    recruiter = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['id', 'created_at','user', 'updated_at']



