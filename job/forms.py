from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import JobListing, Application, CustomUser
from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput
from django.forms import Textarea, TextInput, Select, PasswordInput

class JobListingForm(forms.ModelForm):
    class Meta:
        model = JobListing
        fields = '__all__'
        exclude=['user','locations' ]

        widgets = {

            'title':TextInput(
                attrs={
                   "placeholder": "Enter title",
                   "class": "form-control",
                }
            ),
            'description':TextInput(
               attrs={
                   "placeholder": "Enter description",
                   "class": "form-control",
                }
            ),
            'faculty':TextInput(
               attrs={
                   "placeholder": "Enter faculty",
                   "class": "form-control",
                }
            ),
          
            'category':Select(
               attrs={
                   "placeholder": "Select category",
                   "class": "form-select",
                }
            ),
            'requirements':Textarea(
                attrs={
                    "placeholder": "Enter your bio",
                    "class": "form-control",
                }
            ), 
            'skills':Textarea(
                attrs={
                    "placeholder": "Enter your bio",
                    "class": "form-control",
                }
            ),

           
            'responsibilities':Textarea(
                attrs={
                    "placeholder": "Enter your responsibility",
                    "class": "form-control",
                }
            ), 
            'vacancy':TextInput(
               attrs={
                   "placeholder": "Enter vacancy",
                   "class": "form-control",
                }
            ),
             'location':TextInput(
               attrs={
                   "placeholder": "Enter location",
                   "class": "form-control",
                }
            ),
             'salary':TextInput(
               attrs={
                   "placeholder": "Enter salary",
                   "class": "form-control",
                }
            ),
            'Job_duration':TextInput(
               attrs={
                   
                   "class": "form-control",
                }
            ),
             'application_deadline':DatePickerInput(
               attrs={
                   "placeholder": "Enter date",
                   "class": "form-control",
                }
            ),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume', 'cover_letter']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Apply'))


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username','first_name', 'last_name', 'email', 'password', 'profile_picture']

        
        widgets = {
            
            'bio':Textarea(
                attrs={
                    "placeholder": "Enter your bio",
                    "class": "form-control",
                }
            ), 
            
            'first_name':TextInput(
                attrs={
                   "placeholder": "Enter name",
                   "class": "form-control",
                }
            ),

            'password':PasswordInput(
                attrs={
                   "placeholder": "Enter password",
                   "class": "form-control",
                }
            ),
            'profile-picture':TextInput(
                attrs={
                   
                   "class": "form-control",
                }
            ),
            'last_name':TextInput(
                attrs={
                   "placeholder": "Enter name",
                   "class": "form-control",
                }
            ),
            'email':TextInput(
                attrs={
                   "placeholder": "Enter your email",
                   "class": "form-control",
                }
            ),
            'username':TextInput(
                attrs={
                   "placeholder": "Enter location name",
                   "class": "form-control",
                }
            )
           
            
        }


class CustomReg(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username',  'password']

        widgets = {
            
            'username':TextInput(
                attrs={
                   "placeholder": "Enter username",
                   "class": "form-control",
                }
            ),
            'password':TextInput(
                attrs={
                 
                   "class": "form-control",
                }
            ),
        }
class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name','username', 'email', 'profile_picture', 'bio']

        
        widgets = {
            
            'bio':Textarea(
                attrs={
                    "placeholder": "Enter your bio",
                    "class": "form-control",
                }
            ), 
            
            'first_name':TextInput(
                attrs={
                   "placeholder": "Enter name",
                   "class": "form-control",
                }
            ),
            'profile-picture':TextInput(
                attrs={
                   
                   "class": "form-control",
                }
            ),
            'last_name':TextInput(
                attrs={
                   "placeholder": "Enter name",
                   "class": "form-control",
                }
            ),
            'email':TextInput(
                attrs={
                   "placeholder": "Enter your email",
                   "class": "form-control",
                }
            ),
            'username':TextInput(
                attrs={
                   "placeholder": "Enter location name",
                   "class": "form-control",
                }
            )
           
            
        }
