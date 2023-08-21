from django.urls import path
from .views import*
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('', JobListingListView.as_view(), name="home"),
    path('all-jobs', Alljobs.as_view(), name="all-jobs"),
    path('favourite-job/<int:id>', userFavourite, name="favourite-jobs"),
    path('favourite-job/delete/<int:pk>', UnfavoriteJob.as_view(), name="delete-favourite"),
    path('login/', CustomLoginView, name="login"),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('create-job/', CreateJob.as_view(), name="create-job"),
    path('update-job/<int:pk>', JobUpdate.as_view(), name="update-job"),
    path('update-profile/<int:pk>', ProfileUpdate.as_view(), name="update-profile"),
    path('delete-job/<int:pk>', JobDelete.as_view(), name="delete-job"),
    path('register/', register, name="register"),
    path('all-users/', AllUsers.as_view(), name="all-users"),
     path('my-jobs/<int:pk>', MyJobs.as_view(), name="my-jobs"),
    path('all-users/update/<int:id>', AdminUserUpdate, name="admin-update-user"),
    path('applicant/<int:id>', application, name="application"),
    path('category-jobs/<int:id>', jobByCategory, name="category-jobs"),
    path('applicant/update/<int:id>', applicantUpdate, name="applicantUpdate"),
    path('user-jobs/<int:id>', userJob, name="user-jobs"),
    path('job-details/<int:pk>', JobListingDetailView.as_view(), name="job-details"),
    path('applicant-details/<int:id>', ApplicationDetail, name="applicant-details"),
    path('applicant-details/delete/<int:id>', deleteApplicant, name="applicant-delete"),
    path('job-details/apply/<int:pk>', ApplyForJobView.as_view(), name="apply"),
    path('favourite/<int:pk>', FavoriteJobView.as_view(), name="favourite"),
    path('unfavourite/<int:pk>', UnfavoriteJob.as_view(), name="unfavourite"),

    path('download/<str:filename>', download_file, name='download'),
]
