from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import JobListing, Application, FavoriteJob, JobCategory, CustomUser, Testimonial
from .forms import JobListingForm, UserRegistrationForm, ApplicationForm, CustomReg, ProfileForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .decorator import can_post, is_super
from django.http.response import HttpResponse
import mimetypes
import os

def CustomLoginView(request):
   
    if request.user.is_authenticated:
        return redirect('home')
    #when submit botti=on is pressed 
    if request.method=='POST':  
        username = request.POST.get('username')
        username.lower()
        password = request.POST.get('password')
        
        user=authenticate(request, username=username, password=password)
        if user is not None:
          login(request, user)
          return redirect ('home')
    return render(request, 'job/user/login.html')



def register(request):
    if request.user.is_authenticated:
            return redirect('home')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in.
            login(request, user)
            return redirect('home')  # Redirect to your desired page after registration.
    else:
        form = UserRegistrationForm()
    return render(request, 'job/user/register.html', {'form': form})

class JobListingListView(ListView):
    model = JobListing
    template_name = 'job/home.html'
    context_object_name = 'jobs'
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_jobs"] = JobListing.objects.filter(available=True).count()
        #context["category_jobs"] = JobListing.objects.filter(available=True).count() 
        context["full_time"] = JobListing.objects.filter(Q(available=True) and Q(Job_duration=1))
        context["part_time"] = JobListing.objects.filter(Q(available=True) and Q(Job_duration=2))
        context["contracts"] = JobListing.objects.filter(Q(available=True) and Q(Job_duration=3))
        context["categories"] = JobCategory.objects.all
        context["testimonials"] = Testimonial.objects.all
        
        
        # search_input=self.request.GET.get('search-area') or ''
        # if search_input:
        #   context["tasks"] =context["tasks"].filter(
        #       title__icontains=search_input)  
        # context["search_input"] = search_input
        return context

class JobListingDetailView(DetailView):
    model = JobListing
    template_name = 'job/job_details.html'
    context_object_name = 'job'


class Alljobs(ListView):
    model = JobListing
    template_name = 'job/all_jobs.html'
    context_object_name = 'jobs'
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_jobs"] = JobListing.objects.filter(available=True).count()
       
       
      
        # search_input=self.request.GET.get('search-area') or ''
        # if search_input:
        #   context["tasks"] =context["tasks"].filter(
        #       title__icontains=search_input)  
        # context["search_input"] = search_input
        return context



class JobListingDetailView(DetailView):
    model = JobListing
    template_name = 'job/job_details.html'
    context_object_name = 'job'
    

@method_decorator(login_required, name='dispatch')
class ApplyForJobView(View):
    def post(self, request, pk):
        if request.user.is_authenticated:
            job = get_object_or_404(JobListing, pk=pk)
            resume = request.FILES.get('resume')
            cover_letter = request.POST.get('cover_letter')
            email = request.POST.get('email')
            name = request.POST.get('name')
            website = request.POST.get('website')
            application = Application(job=job, applicant=request.user, resume=resume, website=website,  cover_letter=cover_letter, name=name, email=email)
            application.save()
            return redirect('job-details', pk=pk)
        else:
             return redirect('login')

        

@method_decorator(login_required, name='dispatch')
class FavoriteJobView(View):
    def post(self, request, pk):
        job = get_object_or_404(JobListing, pk=pk)
        favorite, created = FavoriteJob.objects.get_or_create(user=request.user, job=job)
        return redirect('home')

@method_decorator(login_required, name='dispatch')
class UnfavoriteJob(View):
    def post(self, request, pk):
        job = get_object_or_404(JobListing, pk=pk)
        favorite = get_object_or_404(FavoriteJob, user=request.user, job=job.id)
        favorite.delete()
        return redirect('favourite-jobs', request.user.id)
    

@method_decorator([login_required, can_post], name='dispatch')
class CreateJob(View):
    
    def get(self, request):
        pagename="Create Job"
        form = JobListingForm()
        return render(request, 'job/create_job.html', {'form': form, 'pagename':pagename})

    def post(self, request):
        form = JobListingForm(request.POST)
        
        if form.is_valid():
            form.save(commit=False)
            form.user=request.user.id
            form.save()
            return redirect('user-jobs', request.user.id)

        return render(request, 'job/create_job.html', {'form': form})

@method_decorator([login_required, can_post], name='dispatch')
class JobUpdate(UpdateView):
    model=JobListing
    form_class = JobListingForm
    template_name='job/create_job.html'
    success_url=reverse_lazy('home')
    
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(JobUpdate, self).form_valid(form)

@method_decorator([login_required, can_post], name='dispatch')
class JobDelete(DeleteView):
    model=JobListing
    context_object_name='job'
    template_name='job/delete_job.html'
    success_url=reverse_lazy('home')


@login_required(login_url='login')
@can_post
def userJob(request, id):
    pagename="Posted Jobs"
    jobs=JobListing.objects.filter(user=id)
    return render(request, 'job/user/user_job.html', {'jobs':jobs, 'pagename':pagename} )

#Jobs By category
def jobByCategory(request, id):
    jobs=JobListing.objects.filter(category=id)
    count=jobs.count()
    return render(request, 'job/category_job.html', {'jobs':jobs, 'count':count} )


@login_required(login_url='login')
def userFavourite(request, id):
    jobs=FavoriteJob.objects.filter(user=id)
    return render(request, 'job/user/userFavourite_job.html', {'jobs':jobs} )

@login_required(login_url='login')
def application(request, id):
    applicants=Application.objects.filter(applicant=id)
    count=applicants.count()
    # for applicant in applicants:
    #     cvs=str(applicant.resume)
    #     cv=cvs.split('/')[1]

    return render(request, 'job/application.html', {'applicants':applicants, 'count':count} )


@login_required(login_url='login')
@can_post
def ApplicationDetail(request, id):
    applicant=Application.objects.get(pk=id)
    cvs=str(applicant.resume)
    cv=cvs.split('/')[1]
    return render(request, 'job/application_details.html', {'applicant':applicant,  'cv':cv} )


@login_required(login_url='login')
@can_post
def applicantUpdate(request, id):
    if request.method=="POST":
        status=request.POST.get('status')
        applicant=Application.objects.filter(pk=id)
        applicant.update(status=status)
        return redirect('application', request.user.id)

@login_required(login_url='login')
@can_post
def deleteApplicant(request, id):
    if request.method=="POST":      
        Application.objects.filter(pk=id).delete()
        return redirect('application', request.user.id)
    
@method_decorator([login_required, can_post, is_super], name='dispatch')  
class AllUsers(ListView):
    model = CustomUser
    template_name = 'job/user/all_users.html'
    context_object_name = 'users'
    paginate_by = 5
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["count"] = CustomUser.objects.filter().count()
        context["active_count"] = CustomUser.objects.filter(is_active=1).count()
        context["post_count"] = CustomUser.objects.filter(can_post=1).count()
        context["pagename"] = "All Users"
       
        return context
#users applied jobs

@method_decorator([login_required], name='dispatch')  
class MyJobs(ListView):
    model = Application
    template_name = 'job/my_jobs.html'
    context_object_name = 'jobs'
    paginate_by = 5
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["count"] =Application.objects.filter(Q(applicant=self.request.user) ).count()
        context["myjobs"] =Application.objects.filter(Q(applicant=self.request.user) )
        applicants=Application.objects.filter(Q(applicant=self.request.user) )
        
        # for applicant in applicants:
        #     cvs=str(applicant.resume)
        #     cv=cvs.split('/')[1]
        # context["cv"] =cv
        context["pagename"]="My Jobs"
       
        return context

class TestimonyList(ListView):
    model = Testimonial
    template_name = 'job/home.html'
    context_object_name = 'testimonials'
    paginate_by = 5


#download cv
@login_required(login_url='login')
@can_post
@is_super
def AdminUserUpdate(request, id):
    if request.method=="POST":
        can_post=request.POST.get('can_post')
        is_active=request.POST.get('is_active')
        is_admin=request.POST.get('is_admin')
        user=CustomUser.objects.filter(pk=id)
        user.update(can_post=can_post, is_active=is_active, is_superuser=is_admin)
       
        
        #user.update(is_active=is_active,can_post=can_post, is_superuser=is_admin)
        return redirect('all-users')
    

#Profile Update
@method_decorator([login_required], name='dispatch') 
class ProfileUpdate(UpdateView):
    model=CustomUser
    form_class = ProfileForm
    template_name='job/user/profile.html'
    success_url=reverse_lazy('home')
    
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(ProfileUpdate, self).form_valid(form)
    



def download_file(request, filename=''):
    if filename != '':
        # Define Django project base directory
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Define the full file path
        filepath = BASE_DIR + '/uploads/resumes/' + filename
        # Open the file for reading content
        path = open(filepath, 'rb')
        # Set the mime type
        mime_type, _ = mimetypes.guess_type(filepath)
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        # Return the response value
        return response
    else:
        # Load the template
        return render(request, 'home.html')