
from rest_framework import serializers

from .models import Blog, Comment, Job, JobApplication, Posts, Like


class BlogSerializer(serializers.ModelSerializer):

    recruiter = serializers.StringRelatedField(source='user', read_only=True)

    class Meta:
        model = Blog
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']

class BlogCommentSerialzer(serializers.ModelSerializer):
    user=serializers.StringRelatedField(read_only=True)

    class Meta:
        model=Comment
        fields=['id','user','content','created_at']

# 🔹 Job Serializer
class JobSerializer(serializers.ModelSerializer):
    recruiter = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['id', 'created_at','user', 'updated_at']


# 🔹 Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at']


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['id', 'user', 'job', 'applied_at']
        read_only_fields = ['user', 'applied_at',]

# 🔹 Post Serializer
class PostSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    company_name = serializers.SerializerMethodField()

    user = serializers.StringRelatedField(read_only=True)
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj):
        return []  # or limit to 1–2
    
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Posts
        fields = [
            'id',
            'user',
            'title',
            'description',
            'created_at',
            'full_name',
            'company_name',
            'comments',
            'likes_count'
        ]
        read_only_fields = ['id', 'created_at', 'user', 'full_name', 'company_name', 'comments', 'likes_count']

    def get_full_name(self, obj):
    # Recruiter
        if hasattr(obj.user, 'recruiterprofile'):
            return obj.user.recruiterprofile.full_name

        # Seeker
        if hasattr(obj.user, 'seekerprofile'):
            return obj.user.seekerprofile.full_name

        return None

    def get_company_name(self, obj):
        if hasattr(obj.user, 'recruiterprofile'):
            return obj.user.recruiterprofile.company_name
        return None

    def get_likes_count(self, obj):
        return obj.likes.count()


# 🔹 Like Serializer
class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'post']