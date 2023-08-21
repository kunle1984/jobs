from django.contrib import admin
from .models import*

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Faculty)
admin.site.register([Location, JobCategory, Skill, JobListing, JobLocation, FavoriteJob, Application, Testimonial, JobDuration])