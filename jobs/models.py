from django.db import models

class Blog(models.Model):
    user=models.ForeignKey("accounts.RecruiterProfile",
                           related_name="blogs",on_delete=models.CASCADE)
    
    title=models.CharField(max_length=200)
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=["-created_at"]
        verbose_name="Blog"

    def __str__(self):
        return self.title
    
class BlogLike(models.Model):
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE,related_name="likes")
    user=models.ForeignKey("accounts.CustomUser",on_delete=models.CASCADE,related_name="user_blog_likes")
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("blog", "user")
        verbose_name = "Blog Like"
        verbose_name_plural = "Blog Likes"
        constraints = [models.UniqueConstraint(fields=["blog", "user"], name="unique_blog_like")]

    def __str__(self):
        return f"{self.user} likes {self.blog}"


class Job(models.Model):

    user = models.ForeignKey("accounts.RecruiterProfile", related_name="jobs", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(default="No Description Available")
    location = models.CharField(max_length=100)
    stipend = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Job stipend in currency units")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Job"
        verbose_name_plural = "Jobs"

    def __str__(self):
        return self.title


