
from rest_framework import serializers

from .models import Blog, Comment, Job, Posts, Like


class BlogSerializer(serializers.ModelSerializer):

    recruiter=serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Blog
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

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


# 🔹 Post Serializer
class PostSerializer(serializers.ModelSerializer):
    recruiter = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Posts
        fields = ['id', 'recruiter', 'title', 'description', 'created_at', 'comments', 'likes_count']

    def get_likes_count(self, obj):
        return obj.likes.count()


# 🔹 Like Serializer
class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'post']