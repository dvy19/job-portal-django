from django.db import models
from pytz import timezone

# Create your models here.

'''
difference between auto_now_add and auto_now
-created_first and created_first
'''
class Job(models.Model):

    user=models.ForeignKey("accounts.RecruiterProfile", related_name='posts', on_delete=models.CASCADE)

    title=models.CharField(max_length=100)
    description=models.TextField(default="No Description Available")
    location=models.CharField(max_length=100)
    '''
    can store values up to 99,999,999.99 (10 digits total, 2 after decimal).
    Default is 0.00.
    '''
    stipend=models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at=models.DateTimeField(auto_now_add=True )
    updated_at=models.DateTimeField(auto_now=True )

    #newest first, can add more filters later like likes, comments etc
    class Meta:
        ordering=['-created_at']

    def __str__(self):
        return self.title
    

class Posts(models.Model):

    recruiter=models.ForeignKey("accounts.RecruiterProfile", related_name='posts', on_delete=models.CASCADE)

    title=models.CharField(max_length=20)
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):

    post=models.ForeignKey(Posts, related_name='comments', on_delete=models.CASCADE)
    user=models.ForeignKey("accounts.CustomUser", related_name='comments', on_delete=models.CASCADE)

    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.post}"

class Like(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)

    class Meta:
        unique_together = ['post', 'user']  # prevents duplicate likes