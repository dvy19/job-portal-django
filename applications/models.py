from django.db import models

# Create your models here.
class JobApplication(models.Model):
    job = models.ForeignKey("jobs.Job", on_delete=models.CASCADE, related_name='applications')

    seeker = models.ForeignKey('accounts.JobSeekerProfile', on_delete=models.CASCADE, related_name='applications')

    applied_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ('applied', 'Applied'),
            ('shortlisted', 'Shortlisted'),
            ('rejected', 'Rejected')
        ],
        default='applied'
    )

    def __str__(self):
        return f"{self.seeker.full_name} applied for {self.job.title}"