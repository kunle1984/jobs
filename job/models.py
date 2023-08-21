from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True)
    can_post=models.BooleanField(default=False)
    is_applicant=models.BooleanField(default=True)
   # USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username

class Faculty(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    logo = models.ImageField(upload_to='faculty_logos/')
    website = models.URLField()
    location = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class JobCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    icon= models.CharField(max_length=50, null=True, default="fa-book-reader")
    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    def __str__(self):
        return self.name

class JobDuration(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    def __str__(self):
        return self.name

class JobListing(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE )
    title = models.CharField(max_length=100)
    description = models.TextField()
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    Job_duration = models.ForeignKey(JobDuration, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE)
    requirements = models.TextField()
    responsibilities = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    application_deadline = models.DateTimeField()
    skills = models.ManyToManyField(Skill, through='JobSkill')
    locations = models.ManyToManyField(Location, through='JobLocation')
    vacancy=models.CharField(max_length=100)
    location=models.CharField(max_length=100, null=True)
    salary=models.CharField(max_length=100)
    available=models.BooleanField(default=True)
    image=models.ImageField(upload_to='job_image/', blank=True, null=True)
    def __str__(self):
        return self.title

class JobSkill(models.Model):
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    def __str__(self):
        return self.job.title

class JobLocation(models.Model):
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    def __str__(self):
        return self.location.name

class Application(models.Model):
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    email=website=models.EmailField(unique=True)
    applicant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField()
    website=models.CharField(max_length=100, null=True, blank=True)
    name=models.CharField(max_length=100)
    application_date = models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=10, null=True, default=0)
    def __str__(self):
        return self.job.title

class FavoriteJob(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE)
  
    def __str__(self):
        return self.job.title
    

class Testimonial(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
   

