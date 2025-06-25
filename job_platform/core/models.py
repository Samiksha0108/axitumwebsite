

# Create your models here.
# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

# -----------------------------
# Candidate Model
# -----------------------------
# class Candidate(AbstractUser):
#     resume = models.FileField(upload_to='resumes/', null=True, blank=True)
#     phone = models.CharField(max_length=15, blank=True)
#     preferred_skills = models.TextField(null=True, blank=True)  # Comma-separated skills
#     # Add any other candidate-specific fields
class Candidate(AbstractUser):
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    preferred_skills = models.TextField(null=True,blank=True)
    phone = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = "Candidate"
        verbose_name_plural = "Candidates"

# -----------------------------
# Company Model
# -----------------------------
# class Company(models.Model):
#     name = models.CharField(max_length=255)
#     code = models.CharField(max_length=50, unique=True)
#     email = models.EmailField(unique=True)
#     phone = models.CharField(max_length=20, null=True, blank=True)
#     address = models.TextField(null=True, blank=True)
#     industry = models.CharField(max_length=100, null=True, blank=True)
#     description = models.TextField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return self.name


# # -----------------------------
# # Unified Company User Model
# # -----------------------------
# class CompanyUser(models.Model):
#     company = models.ForeignKey(Company, on_delete=models.CASCADE)
#     full_name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=128)  # Use make_password when saving
#     role = models.CharField(max_length=20, choices=[
#         ('admin', 'Admin'),
#         ('hr', 'HR'),
#         ('manager', 'Manager'),
#         ('employee', 'Employee')
#     ])
#     designation = models.CharField(max_length=100, null=True, blank=True)
#     manager = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, limit_choices_to={'role': 'manager'}, related_name='team_members')
#     linked_candidate = models.ForeignKey(Candidate, null=True, blank=True, on_delete=models.SET_NULL)

#     def __str__(self):
#         return f"{self.full_name} ({self.role})"


# models.py
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# class Company(models.Model):
#     name = models.CharField(max_length=255)
#     code = models.CharField(max_length=100, unique=True)  # system-generated after registration
    
#     email = models.EmailField(unique=True)
#     address = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name

# class CompanyUser(models.Model):
#     company = models.ForeignKey(Company, on_delete=models.CASCADE)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=255)
#     role = models.CharField(max_length=20, choices=[
#         ('admin', 'Admin'),
#         ('hr', 'HR'),
#         ('manager', 'Manager'),
#         ('employee', 'Employee')
#     ])
#     #created_at = models.DateTimeField(auto_now_add=True)

#     # New hierarchy field:
#     manager = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subordinates', limit_choices_to={'role': 'manager'})

#     def __str__(self):
#         return f"{self.email} ({self.role})"


# -----------------------------
# Job Model
# -----------------------------

from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class CompanyUser(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=[
        ('admin', 'Admin'),
        ('hr', 'HR'),
        ('manager', 'Manager'),
        ('employee', 'Employee')
    ])
    password = models.CharField(max_length=255)
    manager = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)  # ✅ New field added


    def set_password(self, raw_password):
        from django.contrib.auth.hashers import make_password
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)


class JobRole(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    salary_min = models.DecimalField(max_digits=10, decimal_places=2)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2)
    employment_type = models.CharField(max_length=15, choices=[
        ('full-time', 'Full-time'),
        ('part-time', 'Part-time'),
        ('contract', 'Contract')
    ])
    location = models.CharField(max_length=100)
    experience_level = models.CharField(max_length=10, choices=[
        ('entry', 'Entry'),
        ('mid', 'Mid'),
        ('senior', 'Senior')
    ])
    status = models.CharField(max_length=10, choices=[
        ('open', 'Open'),
        ('closed', 'Closed')
    ], default='open')
    keywords = models.TextField(blank=True)


    def get_keyword_list(self):
        return self.keywords.split(",") if self.keywords else []



# -----------------------------
# Application Model
# -----------------------------
class Application(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    job = models.ForeignKey(JobRole, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('in_progress', 'In Progress'),
        ('applied', 'Applied'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected'),
        ('discarded', 'Discarded'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.username} - {self.job.title}"


# -----------------------------
# Timesheet Model
# -----------------------------
# class Timesheet(models.Model):
#     employee = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, limit_choices_to={'role': 'employee'})
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()
#     hours = models.FloatField()
#     status = models.CharField(max_length=20, choices=[
#         ('submitted', 'Submitted'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected')
#     ])
#     approved_by = models.ForeignKey(CompanyUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='approved_timesheets')
#     submitted_on = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.employee.full_name} - {self.status}"


# models.py

from django.db import models
from datetime import date, time
from decimal import Decimal

class Timesheet(models.Model):
    # company_user = models.ForeignKey('CompanyUser', on_delete=models.CASCADE)
    company_user = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, null=True, blank=True, related_name='timesheets')

    date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    submitted = models.BooleanField(default=False)
    approved = models.BooleanField(null=True, blank=True)  # None = pending, True = approved, False = rejected

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.company_user.email} - {self.date} - {self.hours_worked} hrs"


# -----------------------------
# Project Model (Optional)
# -----------------------------
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    manager = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, limit_choices_to={'role': 'manager'})
    assigned_to = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, related_name='projects', limit_choices_to={'role': 'employee'})
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ])

    def __str__(self):
        return self.name

