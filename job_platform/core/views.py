from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CandidateSignupForm, CandidateLoginForm,CompanySignupForm, EmployeeSignupForm,AddEmployeeForm,ResumeUploadForm
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
# Candidate Signup
from django.http import HttpResponseForbidden
from .forms import JobRoleForm,CompanyLoginForm,CompanySignupForm,TimesheetForm,ResumeUploadForm,HybridSignupForm
from .utils import extract_keywords  # Assuming this function exists
from .models import JobRole, Company, Application, Candidate,CompanyUser,Timesheet
from .utils import extract_text, match_resume_to_job  # assuming you have these utilities
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils.dateparse import parse_date
import json
from datetime import date
from decimal import Decimal
from .utils import get_month_days

def home(request):
    return render(request, 'index.html', {
        'candidate_form': CandidateSignupForm(),
        'form': CandidateLoginForm(),
        'company_login_form': CompanyLoginForm(),
        'company_signup_form': CompanySignupForm(),
        'show_login_modal': False,
        'show_signup_modal': False,
        'show_company_login_modal': False,
        'show_company_signup_modal': False,
    })





def candidate_signup(request):
    if request.method == 'POST':
        form = CandidateSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('candidate_dashboard')
        else:
            return render(request, 'index.html', {
                'candidate_form': form,
                'show_signup_modal': True
            })
    else:
        form = CandidateSignupForm()
        # Inside candidate_signup view
    return render(request, 'index.html', {
        'candidate_form': form,
        'show_signup_modal': True
    })



# Candidate Login
def candidate_login(request):
    if request.method == 'POST':
        form = CandidateLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('candidate_dashboard')
            else:
                messages.error(request, 'Invalid email or password.')
                return render(request, 'index.html', {
                    'form': form,
                    'show_login_modal': True
                })
    else:
        form = CandidateLoginForm()
    return redirect('home')  # or render 'index.html' if needed

# Candidate Logout
def candidate_logout(request):
    logout(request)
    return redirect('candidate_login')

# Candidate Dashboard
from .models import JobRole
# from .forms import ContactForm

def candidate_dashboard(request):
    query = request.GET.get('query', '')
    all_jobs = JobRole.objects.all().order_by('-id')

    if query:
        all_jobs = all_jobs.filter(title__icontains=query)

    return render(request, 'candidate_dashboard.html', {
        'all_jobs': all_jobs,
        'query': query,
        # 'contact_form': ContactForm(),
    })




def company_signup_placeholder(request):
    return HttpResponse("Company signup is under construction. Please check back soon.")





# def company_signup(request):
#     if request.method == 'POST':
#         form = CompanySignupForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data

#             # Employee Registration Flow
#             if data.get('is_employee'):
#                 try:
#                     company = Company.objects.get(code=data['company_code'])
#                     user = CompanyUser(
#                         company=company,
#                         email=data['email'],
#                         role=data['role'],
#                         password=make_password(data['password1'])
#                     )
#                     user.save()

#                     request.session['company_id'] = company.id
#                     request.session['company_user_id'] = user.id
#                     request.session['role'] = user.role
#                     return redirect('company_dashboard')

#                 except Company.DoesNotExist:
#                     messages.error(request, 'Invalid company code.')
#                     return redirect('home')

#             # Company Admin Registration Flow
#             else:
#                 # Generate a unique 6-digit company code
#                 code = 'CMP' + str(uuid.uuid4().int)[:6]

#                 company = Company(
#                     name=data['name'],
#                     email=data['email'],
#                     address=data['address'],
#                     code=code,
#                 )
#                 company.save()

#                 # Send the code via email
#                 send_mail(
#                     subject='Your Company Registration Code',
#                     message=(
#                         f"Hello {company.name},\n\n"
#                         f"Thank you for registering your company on ACME ATS.\n"
#                         f"Please share this code with your employees: {code}\n\n"
#                         f"Regards,\nACME Team"
#                     ),
#                     from_email='samikshareddy789@gmail.com',
#                     recipient_list=[company.email],
#                     fail_silently=False,
#                 )

#                 user = CompanyUser(
#                     company=company,
#                     email=data['email'],
#                     role='admin',
#                     password=make_password(data['password1'])  # Hash at creation
#                 )
#                 user.save()


#                 request.session['company_id'] = company.id
#                 request.session['company_user_id'] = user.id
#                 request.session['role'] = user.role
#                 return redirect('company_dashboard')

#         else:
#             messages.error(request, 'Please correct the form errors.')
           
#             return render(request, 'index.html', {
#                 'company_signup_form': form,
#                 'show_company_signup_modal': True,
#                 'show_company_login_modal': False,
#                 'show_login_modal': False,
#                 'show_signup_modal': False,
#             })


#     # GET request fallback
#     form = CompanySignupForm()
#     return redirect('home')



# Company Signup View
def company_signup(request):
    if request.method == 'POST':
        form = CompanySignupForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.code = 'CMP' + str(uuid.uuid4().int)[:6]
            company.save()

            # Send email with code (optional for now)
            send_mail(
                subject='Your Company Code',
                message=f"Welcome {company.name}, your company code is: {company.code}",
                from_email='admin@axitem.com',
                recipient_list=[company.email],
                fail_silently=False,
            )

            # Create first admin user
            admin_user = CompanyUser(
                company=company,
                email=company.email,
                role='admin',
                password=make_password(form.cleaned_data['password1'])
            )
            admin_user.save()

            request.session['company_user_id'] = admin_user.id
            request.session['company_id'] = company.id
            request.session['role'] = 'admin'
            return redirect('company_dashboard')

    else:
        form = CompanySignupForm()
    return render(request, 'company_signup.html', {'form': form})


# Employee Signup View
def employee_signup(request):
    if request.method == 'POST':
        form = EmployeeSignupForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['company_code']
            try:
                company = Company.objects.get(code=code)
            except Company.DoesNotExist:
                form.add_error('company_code', 'Invalid company code')
                return render(request, 'employee_signup.html', {'form': form})

            user = CompanyUser(
                company=company,
                email=form.cleaned_data['email'],
                role='employee',  # default role at signup
                password=make_password(form.cleaned_data['password1'])
            )
            user.save()

            request.session['company_user_id'] = user.id
            request.session['company_id'] = company.id
            request.session['role'] = 'employee'
            return redirect('employee_dashboard')

    else:
        form = EmployeeSignupForm()
    return render(request, 'employee_signup.html', {'form': form})


# Company Login



def company_login(request):
    if request.method == 'POST':
        form = CompanyLoginForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            try:
                company = Company.objects.get(code=code)
                user = CompanyUser.objects.get(email=email, company=company)

                from django.contrib.auth.hashers import check_password
                if check_password(password, user.password):
                    request.session['company_id'] = company.id
                    request.session['company_user_id'] = user.id
                    request.session['role'] = user.role
                    return redirect('company_dashboard')
                else:
                    messages.error(request, 'Invalid password.')
            except (Company.DoesNotExist, CompanyUser.DoesNotExist):
                messages.error(request, 'Invalid company code or email.')
        else:
            messages.error(request, 'Please correct the form errors.')

        # 🟨 Re-render index.html with modal open
        return render(request, 'index.html', {
            'company_login_form': form,
            'show_company_login_modal': True,
            'show_company_signup_modal': False,
            'show_login_modal': False,
            'show_signup_modal': False,
        })

    return redirect('home')



# def company_dashboard_view(request):
#     company_id = request.session.get('company_id')
#     if not company_id:
#         return redirect('company_login')

#     company = Company.objects.get(id=company_id)
#     job_posts = JobRole.objects.filter(company=company,status='open')

#     # employees = Employee.objects.filter(company=company)

#     return render(request, 'company_dashboard.html', {
#         'company': company,
#         'job_posts': job_posts,
#         # 'employees': employees,
#     })



def company_dashboard_view(request):
    company_id = request.session.get('company_id')
    user_id = request.session.get('company_user_id')
    role = request.session.get('role')

    if not company_id or not user_id:
        return redirect('company_login')

    company = Company.objects.get(id=company_id)
    user = CompanyUser.objects.get(id=user_id)

    # Handle job posts only for admin/hr
    job_posts = []
    if role in ['admin', 'hr']:
        job_posts = JobRole.objects.filter(company=company)

    # Handle resume upload only for employees
    form = None
    if role == 'employee':
        if request.method == 'POST':
            form = ResumeUploadForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                return redirect('company_dashboard')  # After successful upload, refresh page
        else:
            form = ResumeUploadForm(instance=user)

    return render(request, 'company_dashboard.html', {
        'company': company,
        'job_posts': job_posts,
        'role': role,
        'form': form,
        'user': user
    })





def add_employee(request):
    if request.method == 'POST':
        form = AddEmployeeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            role = form.cleaned_data['role']

            company_id = request.session.get('company_id')
            company = Company.objects.get(id=company_id)

            # ✅ Check if this email already exists under company
            existing_user = CompanyUser.objects.filter(company=company, email=email).first()
            if existing_user:
                messages.warning(request, f"{email} already exists in your company.")
                return redirect('add_employee')

            # ✅ Create placeholder user with empty password
            CompanyUser.objects.create(
                company=company,
                email=email,
                role=role,
                password=''  # Empty password (will be set during signup)
            )

            # ✅ Send invitation email
            send_mail(
                subject='You’ve been invited to join ACME ATS',
                message=(
                    f"Hello,\n\nYou have been invited to join {company.name} as {role}.\n\n"
                    f"To complete your signup, go to: https://your-domain.com/signup/\n"
                    f"Your Company Code: {company.code}\n\n"
                    f"Please signup with your same email address."
                ),
                from_email='your_email@gmail.com',
                recipient_list=[email],
                fail_silently=False,
            )

            messages.success(request, f"Invitation sent to {email}.")
            return redirect('company_dashboard')
    else:
        form = AddEmployeeForm()
    return render(request, 'add_employee.html', {'form': form})






def post_job(request):
    company_id = request.session.get('company_id')
    user_id = request.session.get('company_user_id')
    role = request.session.get('role')

    # 🚫 Not logged in
    if not company_id or not user_id:
        return redirect('company_login')

    # ❌ Not admin or HR
    if role not in ['admin', 'hr']:
        return HttpResponseForbidden("Only Admins or HRs can post jobs.")

    # ✅ Get company and user
    try:
        company = Company.objects.get(id=company_id)
        user = CompanyUser.objects.get(id=user_id, company=company)
    except (Company.DoesNotExist, CompanyUser.DoesNotExist):
        return redirect('company_login')

    description = None
    keywords_choices = []

    if request.method == 'POST':
        description = request.POST.get('description')
        if description:
            keywords_choices = extract_keywords(description)

        form = JobRoleForm(request.POST)
        form.fields['selected_keywords'].choices = [(kw, kw) for kw in sorted(keywords_choices)]

        if 'preview_keywords' in request.POST:
            return render(request, 'post_job.html', {'form': form})

        elif form.is_valid():
            job = form.save(commit=False)
            job.company = company

            # Keywords
            selected_keywords = form.cleaned_data.get('selected_keywords', [])
            if isinstance(selected_keywords, str):
                selected_keywords = [selected_keywords]

            manual_keywords = form.cleaned_data.get('manual_keywords', '')
            manual_list = [kw.strip() for kw in manual_keywords.split(',') if kw.strip()]
            job.keywords = ",".join(selected_keywords + manual_list)

            job.save()
            return redirect('company_dashboard')

    else:
        form = JobRoleForm()

    return render(request, 'post_job.html', {'form': form})




def job_detail_company(request, job_id):
    company_id = request.session.get('company_id')
    company_user_id = request.session.get('company_user_id')
    role = request.session.get('role')

    if not company_id or not company_user_id:
        return redirect('company_login')

    if role not in ['admin', 'hr']:
        return HttpResponseForbidden("Only Admin or HR can view job details.")

    company = get_object_or_404(Company, id=company_id)
    job = get_object_or_404(JobRole, id=job_id, company=company)

    return render(request, 'job_detail_company.html', {
        'job': job
    })




def close_job(request, job_id):
    company_id = request.session.get('company_id')
    company_user_id = request.session.get('company_user_id')
    role = request.session.get('role')

    if not company_id or not company_user_id:
        return redirect('company_login')

    if role not in ['admin', 'hr']:
        return HttpResponseForbidden("Only Admin or HR can close job postings.")

    company = get_object_or_404(Company, id=company_id)
    job = get_object_or_404(JobRole, id=job_id, company=company)

    # Soft close: mark job status as closed
    job.status = 'closed'
    job.save()

    messages.success(request, "Job has been successfully closed.")
    return redirect('company_dashboard')




def job_matches(request, job_id):
    # ✅ Verify session-based login and role
    company_id = request.session.get('company_id')
    role = request.session.get('role')

    if not company_id or not role:
        return redirect('company_login')

    if role not in ['admin', 'hr']:
        return HttpResponseForbidden("Only Admin or HR can view matches.")

    company = get_object_or_404(Company, id=company_id)
    job = get_object_or_404(JobRole, id=job_id, company=company)

    matches = []

    if request.method == 'POST':
        matches = []
        candidates = Candidate.objects.exclude(resume='')

        for candidate in candidates:
            resume_path = candidate.resume.path
            try:
                resume_text = extract_text(resume_path)
                score, matched_keywords = match_resume_to_job(resume_text, job.keywords)
                if score > 0:
                    matches.append({
                        'name': candidate.get_full_name(),
                        'email': candidate.email,
                        'score': score,
                        'matched_keywords': list(matched_keywords),
                        'resume_url': candidate.resume.url,
                    })
            except Exception as e:
                print(f"Error processing resume {resume_path}: {e}")

        matches = sorted(matches, key=lambda x: x['score'], reverse=True)[:10]


    return render(request, 'job_detail_company.html', {
        'job': job,
        'matches': matches
    })



def suggested_jobs(request):
    candidate = request.user  # Assuming user is logged-in Candidate
    preferred_skills = candidate.preferred_skills

    # Convert preferred_skills string to set
    candidate_skills = set(skill.strip().lower() for skill in preferred_skills.split(',') if skill.strip())

    all_jobs = JobRole.objects.all()
    job_matches = []

    for job in all_jobs:
        job_keywords = set(kw.strip().lower() for kw in job.keywords.split(',') if kw.strip())
        matched_keywords = candidate_skills & job_keywords
        score = len(matched_keywords)

        if score > 0:
            job_matches.append({
                'job': job,
                'score': score,
                'matched_keywords': matched_keywords
            })

    # Sort by score descending
    job_matches.sort(key=lambda x: x['score'], reverse=True)

    return render(request, 'suggested_jobs.html', {'matches': job_matches})



# def job_detail_candidate(request, id):
#     job = get_object_or_404(JobRole, id=id)

#     if job.status != 'open':
#         return HttpResponseForbidden("This job is no longer available.")

#     context = {
#         'job': job,
#         'keywords': job.get_keyword_list(),
#     }
#     return render(request, 'job_detail_candidate.html', context)


@login_required
def job_detail_candidate(request, job_id):
    job = get_object_or_404(JobRole, id=job_id)
    candidate = request.user
    application = Application.objects.filter(candidate=candidate, job=job).first()

    return render(request, 'job_detail_candidate.html', {
        'job': job,
        'application': application,
    })




@login_required
def start_application(request, job_id):
    job = get_object_or_404(JobRole, id=job_id)
    candidate = request.user  # AUTH_USER_MODEL is Candidate
    existing_application = Application.objects.filter(candidate=candidate, job=job).first()

    if not existing_application:
        Application.objects.create(candidate=candidate, job=job, status='in_progress')

    return redirect('continue_application', job_id=job_id)

@login_required
def continue_application(request, job_id):
    job = get_object_or_404(JobRole, id=job_id)
    candidate = request.user
    application = get_object_or_404(Application, candidate=candidate, job=job)

    if request.method == 'POST':
        if 'submit' in request.POST:
            application.status = 'applied'
            application.save()
            return redirect('candidate_dashboard')
        elif 'cancel' in request.POST:
            application.status = 'discarded'
            application.save()
            return redirect('candidate_dashboard')

    return render(request, 'apply_form.html', {'job': job, 'application': application})


# views.py


def job_applications(request, job_id):
    company_id = request.session.get('company_id')
    role = request.session.get('role')

    if not company_id or not role:
        return redirect('company_login')

    if role not in ['admin', 'hr']:
        return HttpResponseForbidden("Only Admin or HR can view applications.")

    company = get_object_or_404(Company, id=company_id)
    job = get_object_or_404(JobRole, id=job_id, company=company)

    applications = Application.objects.filter(job=job, status='applied').select_related('candidate')


    return render(request, 'job_applications.html', {
        'job': job,
        'applications': applications,
    })




def view_employees(request):
    company_id = request.session.get('company_id')
    company_user_id = request.session.get('company_user_id')
    role = request.session.get('role')

    if not company_id or not role:
        return redirect('company_login')

    company = get_object_or_404(Company, id=company_id)
    employees = CompanyUser.objects.filter(company=company).order_by('role')

    return render(request, 'view_employees.html', {
        'company': company,
        'employees': employees
    })



def assign_manager(request):
    company_id = request.session.get('company_id')
    if not company_id:
        return redirect('company_login')

    company = get_object_or_404(Company, id=company_id)
    employees = CompanyUser.objects.filter(company=company).exclude(role='admin')
    managers = CompanyUser.objects.filter(company=company, role='manager')

    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        manager_id = request.POST.get('manager_id')

        employee = get_object_or_404(CompanyUser, id=employee_id, company=company)

        if manager_id and manager_id.isdigit():
            manager = get_object_or_404(CompanyUser, id=int(manager_id), company=company, role='manager')
            employee.manager = manager
        else:
            employee.manager = None

        employee.save()
        return redirect('assign_manager')

    return render(request, 'assign_manager.html', {
        'employees': employees,
        'managers': managers
    })



#timesheets
# views.py



def submit_timesheet(request):
    company_id = request.session.get('company_id')
    company_user_id = request.session.get('company_user_id')
    role = request.session.get('role')

    if not company_id or not company_user_id or role != 'employee':
        return redirect('company_login')

    user = get_object_or_404(CompanyUser, id=company_user_id)

    today = date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    selected_str = request.GET.get('selected')
    selected_date = date.fromisoformat(selected_str) if selected_str else today

    month_days = get_month_days(year, month)

    # Handle form submission
    if request.method == 'POST':
        form = TimesheetForm(request.POST)
        if form.is_valid():
            ts = form.save(commit=False)
            ts.company_user = user
            ts.submitted = False
            ts.approved = None
            ts.save()
            messages.success(request, "Timesheet saved!")
            return redirect(f"/submit_timesheet/?year={year}&month={month}&selected={selected_date}")
    else:
        form = TimesheetForm(initial={'date': selected_date})

    # Retrieve submitted entries for calendar highlights
    entry_dates = set(
        Timesheet.objects.filter(
            company_user=user,
            date__year=year,
            date__month=month
        ).values_list('date', flat=True)
    )

    preview_entries = Timesheet.objects.filter(company_user=user, date=selected_date)

    return render(request, 'submit_timesheet.html', {
        'form': form,
        'month_days': month_days,
        'year': year,
        'month': month,
        'selected_date': selected_date,
        'entry_dates': entry_dates,
        'preview_entries': preview_entries,
    })

def submit_all_for_approval(request):
    company_user_id = request.session.get('company_user_id')  # ✅ This was the problem
    role = request.session.get('role')

    if not company_user_id or role != 'employee':
        return redirect('company_login')

    user = get_object_or_404(CompanyUser, id=company_user_id)

    Timesheet.objects.filter(company_user=user, submitted=False).update(submitted=True, approved=None)

    messages.success(request, "All timesheets submitted for approval!")
    return redirect('submit_timesheet')



from .models import Timesheet

def manager_approval(request):
    company_user_id = request.session.get('company_user_id')
    role = request.session.get('role')

    if not company_user_id or role != 'manager':
        return redirect('company_login')

    manager = get_object_or_404(CompanyUser, id=company_user_id)

    # Get employees under this manager
    team = CompanyUser.objects.filter(manager=manager)

    # Get pending timesheets for these employees
    pending_timesheets = Timesheet.objects.filter(
        company_user__in=team,
        submitted=True,
        approved__isnull=True
    ).order_by('date', 'company_user')

    return render(request, 'manager_approval.html', {
        'timesheets': pending_timesheets
    })




def approve_timesheet(request, ts_id):
    company_user_id = request.session.get('company_user_id')
    role = request.session.get('role')

    if not company_user_id or role != 'manager':
        return redirect('company_login')

    timesheet = get_object_or_404(Timesheet, id=ts_id)

    if timesheet.company_user.manager and timesheet.company_user.manager.id == company_user_id:
        timesheet.approved = True
        timesheet.save()

    return redirect('manager_approval')


def reject_timesheet(request, ts_id):
    company_user_id = request.session.get('company_user_id')
    role = request.session.get('role')

    if not company_user_id or role != 'manager':
        return redirect('company_login')

    timesheet = get_object_or_404(Timesheet, id=ts_id)

    if timesheet.company_user.manager and timesheet.company_user.manager.id == company_user_id:
        timesheet.approved = False
        timesheet.save()

    return redirect('manager_approval')



def view_timesheets(request):
    company_user_id = request.session.get('company_user_id')
    role = request.session.get('role')

    if not company_user_id or role != 'employee':
        return redirect('company_login')

    return render(request, 'view_timesheets.html')


def get_approved_timesheets(request):
    company_user_id = request.session.get('company_user_id')
    role = request.session.get('role')

    if not company_user_id or role != 'employee':
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    employee = get_object_or_404(CompanyUser, id=company_user_id)

    # Get all approved timesheets
    timesheets = Timesheet.objects.filter(company_user=employee, approved=True)

    events = []
    for ts in timesheets:
        events.append({
            'title': 'Approved',
            'start': ts.date.strftime('%Y-%m-%d'),
            'allDay': True
        })

    return JsonResponse(events, safe=False)


def get_timesheets_by_date(request):
    company_user_id = request.session.get('company_user_id')
    role = request.session.get('role')

    if not company_user_id or role != 'employee':
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    employee = get_object_or_404(CompanyUser, id=company_user_id)

    date_str = request.GET.get('date')
    selected_date = parse_date(date_str)

    timesheets = Timesheet.objects.filter(
        company_user=employee,
        approved=True,
        date=selected_date
    ).values('start_time', 'end_time', 'hours_worked')

    return JsonResponse({'timesheets': list(timesheets)})





def hybrid_signup(request):
    if request.method == 'POST':
        form = HybridSignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            if data.get('is_employee'):
                company_code = data['company_code']
                email = data['email']

                # First check if company exists
                try:
                    company = Company.objects.get(code=company_code)
                except Company.DoesNotExist:
                    messages.error(request, "Invalid Company Code")
                    return render(request, 'company_signup.html', {'form': form})

                # Company exists — now check if pre-created employee record exists
                try:
                    existing_user = CompanyUser.objects.get(company=company, email=email)

                    if existing_user.password:
                        messages.error(request, "This user is already registered.")
                        return render(request, 'company_signup.html', {'form': form})

                    # Complete signup — fill missing password now
                    existing_user.password = make_password(data['password1'])
                    existing_user.save()

                    request.session['company_user_id'] = existing_user.id
                    request.session['company_id'] = company.id
                    request.session['role'] = existing_user.role
                    return redirect('company_dashboard')

                except CompanyUser.DoesNotExist:
                    messages.error(request, "You are not pre-approved. Contact your admin.")
                    return render(request, 'company_signup.html', {'form': form})

            else:
                # Company signup flow
                code = 'CMP' + str(uuid.uuid4().int)[:6]

                company = Company.objects.create(
                    name=data['name'],
                    address=data['address'],
                    email=data['email'],
                    code=code
                )

                # Send email with company code
                send_mail(
                    subject='Your Company Code',
                    message=f"Your company registration code is: {code}",
                    from_email='admin@axitem.com',
                    recipient_list=[company.email],
                    fail_silently=False,
                )

                admin_user = CompanyUser.objects.create(
                    company=company,
                    email=data['email'],
                    role='admin',
                    password=make_password(data['password1'])
                )

                request.session['company_user_id'] = admin_user.id
                request.session['company_id'] = company.id
                request.session['role'] = admin_user.role
                return redirect('company_dashboard')

    else:
        form = HybridSignupForm()

    return render(request, 'company_signup.html', {'form': form})



def upload_resume_view(request):
    company_user_id = request.session.get('company_user_id')
    role = request.session.get('role')

    if role != 'employee' or not company_user_id:
        return redirect('company_dashboard')

    user = get_object_or_404(CompanyUser, id=company_user_id)

    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('upload_resume')  # refresh the page after upload
    else:
        form = ResumeUploadForm(instance=user)

    return render(request, 'upload_resume.html', {
        'form': form,
        'user': user
    })




def hr_job_board(request):
    company_user_id = request.session.get('company_user_id')
    role = request.session.get('role')

    if role != 'hr' or not company_user_id:
        return redirect('company_dashboard')

    jobs = JobRole.objects.filter(status='open')  # Show only open jobs globally

    return render(request, 'hr_job_board.html', {
        'jobs': jobs,
        'company_user_id': company_user_id,
    })




def hr_job_detail(request, job_id):
    company_user_id = request.session.get('company_user_id')
    role = request.session.get('role')

    if role != 'hr' or not company_user_id:
        return redirect('company_dashboard')

    job = get_object_or_404(JobRole, id=job_id)

    return render(request, 'hr_job_detail.html', {
        'job': job
    })

def send_resumes_view(request, job_id):
    company_user_id = request.session.get('company_user_id')
    role = request.session.get('role')

    if role != 'hr' or not company_user_id:
        return redirect('company_dashboard')

    job = get_object_or_404(JobRole, id=job_id)
    hr_user = CompanyUser.objects.get(id=company_user_id)

    if request.method == 'POST':
        selected_employee_ids = request.POST.getlist('selected_employees')

        employees = CompanyUser.objects.filter(
            id__in=selected_employee_ids,
            company=hr_user.company,
            role='employee',
            resume__isnull=False
        )

        # ⚠ Simulate sending email with resumes
        for emp in employees:
            print(f"Simulating email attachment for: {emp.email} - Resume: {emp.resume.url}")

        # You can implement real email logic here if needed
        messages.success(request, "Resumes have been successfully submitted!")
        return redirect('hr_job_board')

    # Show employee selection form
    employees = CompanyUser.objects.filter(
        company=hr_user.company,
        role='employee',
        resume__isnull=False
    )

    return render(request, 'send_resumes.html', {
        'job': job,
        'employees': employees
    })
