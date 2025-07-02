from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Candidate

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

from django import forms
from django.core.exceptions import ValidationError
from .models import Candidate

class CandidateSignupForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, required=True, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, required=True, label="Confirm Password")

    class Meta:
        model = Candidate
        fields = ['email', 'phone', 'preferred_skills', 'resume']
        widgets = {
            'preferred_skills': forms.Textarea(attrs={'required': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['phone'].required = True
        self.fields['preferred_skills'].required = True
        self.fields['resume'].required = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Candidate.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise ValidationError("Passwords do not match.")
        return cleaned_data


class CandidateLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

# forms.py
from django import forms
from .models import Company, CompanyUser

# class CompanySignupForm(forms.Form):
#     is_employee = forms.BooleanField(required=False)
#     name = forms.CharField(required=False)
#     address = forms.CharField(widget=forms.Textarea, required=False)
#     company_code = forms.CharField(required=False)
#     email = forms.EmailField()
#     password1 = forms.CharField(widget=forms.PasswordInput)
#     password2 = forms.CharField(widget=forms.PasswordInput)
#     role = forms.ChoiceField(choices=[('admin', 'Admin'), ('hr', 'HR'), ('manager', 'Manager'),('employee','Employee')], required=False)

#     def clean(self):
#         cleaned_data = super().clean()
#         if cleaned_data.get('password1') != cleaned_data.get('password2'):
#             raise forms.ValidationError("Passwords do not match")

#         if cleaned_data.get('is_employee'):
#             if not cleaned_data.get('company_code'):
#                 raise forms.ValidationError("Company code is required for employees")
#             if not cleaned_data.get('role') or cleaned_data.get('role') == 'admin':
#                 raise forms.ValidationError("Role must be HR or Manager for employees")
#         else:
#             if not cleaned_data.get('name') or not cleaned_data.get('address'):
#                 raise forms.ValidationError("Name and address are required for company registration")
#         return cleaned_data

from django import forms
from .models import Company

from django import forms
from .models import Company

class CompanySignupForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Company
        fields = ['name', 'email', 'address']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

class EmployeeSignupForm(forms.Form):
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    company_code = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data



class CompanyLoginForm(forms.Form):
    email = forms.EmailField()
    code = forms.CharField(label="Company Code")
    password = forms.CharField(widget=forms.PasswordInput)

from django import forms

class AddEmployeeForm(forms.Form):
    email = forms.EmailField(label="Employee Email")
    role = forms.ChoiceField(choices=[
        ('hr', 'HR'),
        ('manager', 'Manager'),
        ('employee', 'Employee')
    ])

from django import forms
from .models import CompanyUser

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = CompanyUser
        fields = ['resume']

from .models import JobRole
#Job Form
class JobRoleForm(forms.ModelForm):
    selected_keywords = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Select Extracted Keywords"
    )
    manual_keywords = forms.CharField(
        required=False,
        label="Add Your Own Keywords (comma-separated)",
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Leadership, Communication'})
    )

    class Meta:
        model = JobRole
        fields = ['title', 'description', 'salary_min', 'salary_max', 'employment_type', 'location', 'experience_level']


from django import forms
from .models import CompanyUser

class AssignManagerForm(forms.ModelForm):
    class Meta:
        model = CompanyUser
        fields = ['manager']

    employee = forms.ModelChoiceField(queryset=CompanyUser.objects.none(), label="Select Employee")

    def __init__(self, company, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee'].queryset = CompanyUser.objects.filter(company=company).exclude(role='manager')
        self.fields['manager'].queryset = CompanyUser.objects.filter(company=company, role='manager')


from django import forms
from .models import Timesheet

from datetime import datetime

class TimesheetForm(forms.ModelForm):
    class Meta:
        model = Timesheet
        fields = ['date', 'start_time', 'end_time', 'hours_worked']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'hours_worked': forms.NumberInput(attrs={'readonly': 'readonly'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_time')
        end = cleaned_data.get('end_time')

        if start and end:
            if end <= start:
                raise forms.ValidationError("End time must be after start time.")
            delta = datetime.combine(datetime.today(), end) - datetime.combine(datetime.today(), start)
            cleaned_data['hours_worked'] = round(delta.total_seconds() / 3600, 2)

        return cleaned_data


from django import forms

class HybridSignupForm(forms.Form):
    # Common field for employee toggle
    is_employee = forms.BooleanField(required=False, label="Registering as Employee?")
    
    # Company fields
    name = forms.CharField(required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    
    # Employee field
    company_code = forms.CharField(required=False)
    
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        is_employee = cleaned_data.get('is_employee')

        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            raise forms.ValidationError("Passwords do not match")

        if is_employee:
            # Employee flow
            if not cleaned_data.get('company_code'):
                raise forms.ValidationError("Company code is required for employees")
        else:
            # Company flow
            if not cleaned_data.get('name') or not cleaned_data.get('address'):
                raise forms.ValidationError("Company Name and Address are required")

        return cleaned_data


from django import forms
from .models import Candidate

from django.core.exceptions import ValidationError

class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = [
            'first_name', 'last_name', 'email',
            'phone', 'preferred_skills',
            'address', 'linkedin', 'preferred_location',
            'resume',
        ]
        widgets = {
            'preferred_skills': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')

        # Skip validation if resume wasn't re-uploaded
        if resume and hasattr(resume, 'content_type'):
            valid_mime_types = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
            if resume.content_type not in valid_mime_types:
                raise forms.ValidationError('Unsupported file type. Only PDF, DOC, and DOCX are allowed.')

        return resume



from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(label='Your Email')
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), label='Describe Your Issue')

from django import forms
from .models import CompanyUser

class CompanyUserProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyUser
        fields = [
            'phone', 'address', 'linkedin',
            'ssn', 'govt_id', 'resume'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
        }


from django import forms

class CompanySupportForm(forms.Form):
    name = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(label='Your Email')
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), label='Describe Your Issue')
