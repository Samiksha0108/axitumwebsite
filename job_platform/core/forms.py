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

class TimesheetForm(forms.ModelForm):
    class Meta:
        model = Timesheet
        fields = ['date', 'start_time', 'end_time', 'hours_worked']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }


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
