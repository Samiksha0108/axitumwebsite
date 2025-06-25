# core/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    # path('dashboard/', views.candidate_dashboard, name='candidate_dashboard'),
    path('candidate/signup/', views.candidate_signup, name='candidate_signup'),
    path('candidate/login/', views.candidate_login, name='candidate_login'),
    path('candidate/login/', views.candidate_logout, name='candidate_logout'),
    path('candidate/dashboard/', views.candidate_dashboard, name='candidate_dashboard'),
    # path('company/signup/', views.company_signup, name='company_signup'),
    path('company/signup/', views.company_signup, name='company_signup'),
    path('employee/signup/', views.employee_signup, name='employee_signup'),
    path('company/login/', views.company_login, name='company_login'),
    path('company/dashboard/', views.company_dashboard_view, name='company_dashboard'),
    path('company/add-employee/', views.add_employee, name='add_employee'),
    path('company/post-job/', views.post_job, name='post_job'),
    # urls.py
    path('company/job/<int:job_id>/', views.job_detail_company, name='job_detail_company'),
    path('company/job/<int:pk>/close/', views.close_job, name='close_job'),
    path('company/job/<int:job_id>/matches/', views.job_matches, name='job_matches'),
    path('candidate/suggested-jobs/', views.suggested_jobs, name='suggested_jobs'),
    # path('candidate/job/<int:id>/', views.job_detail_candidate, name='job_detail_candidate'),
    path('candidate/job/<int:job_id>/', views.job_detail_candidate, name='job_detail_candidate'),

    path('candidate/job/<int:job_id>/apply/', views.start_application, name='start_application'),
    path('candidate/job/<int:job_id>/continue/', views.continue_application, name='continue_application'),
    path('company/job/<int:job_id>/applications/', views.job_applications, name='job_applications'),
    path('company/employees/', views.view_employees, name='view_employees'),
    path('company/assign-manager/', views.assign_manager, name='assign_manager'),
    # urls.py

    path('submit_timesheet/', views.submit_timesheet, name='submit_timesheet'),
    path('submit_all_for_approval/', views.submit_all_for_approval, name='submit_all_for_approval'),
    path('manager_approval/', views.manager_approval, name='manager_approval'),
    path('approve_timesheet/<int:ts_id>/', views.approve_timesheet, name='approve_timesheet'),
    path('reject_timesheet/<int:ts_id>/', views.reject_timesheet, name='reject_timesheet'),
    # path('view-timesheets/', views.view_timesheets, name='view_timesheets'),
    # path('get-timesheets-by-date/', views.get_timesheets_by_date, name='get_timesheets_by_date'),
    path('view-timesheets/', views.view_timesheets, name='view_timesheets'),
    path('api/approved-timesheets/', views.get_approved_timesheets, name='get_approved_timesheets'),
    path('api/timesheets-by-date/', views.get_timesheets_by_date, name='get_timesheets_by_date'),
    path('signup/', views.hybrid_signup, name='hybrid_signup'),
    path('upload-resume/', views.upload_resume_view, name='upload_resume'),
    path('hr/jobs/', views.hr_job_board, name='hr_job_board'),
    path('hr/job/<int:job_id>/', views.hr_job_detail, name='job_detail_hr'),
    path('hr/job/<int:job_id>/send-resumes/', views.send_resumes_view, name='send_resumes'),












]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)