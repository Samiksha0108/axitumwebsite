
# Register your models here.
from django.contrib import admin
from .models import Candidate, Company, CompanyUser, JobRole, Application, Timesheet, Project

admin.site.register(Candidate)
admin.site.register(Company)
admin.site.register(CompanyUser)
admin.site.register(JobRole)
admin.site.register(Application)
admin.site.register(Timesheet)
admin.site.register(Project)
