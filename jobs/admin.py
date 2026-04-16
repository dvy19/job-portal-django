from django.contrib import admin

from .models import Blog, BlogLike, Job

# Register your models here.
admin.site.register(Blog)
admin.site.register(BlogLike)
admin.site.register(Job)
