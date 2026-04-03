from django.db import models

# Create your models here.

class Job(models.Model):

    user=models.ForeignKey("accounts.RecruiterProfile", related_name='jobs', on_delete=models.CASCADE)

    title=models.CharField(max_length=100)
    description=models.TextField()
    location=models.CharField(max_length=100)
    stipend=models.DecimalField(max_digits=10, decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
