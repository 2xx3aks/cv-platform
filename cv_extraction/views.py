"""
Views for CV extraction app.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import User
from .forms import CVUploadForm, StudentFilterForm, StudentComparisonForm, CVProfileEditForm
from .cv_extractor import CVExtractor
from .mongodb_utils import (
    save_cv_profile, get_cv_profile, get_all_cv_profiles,
    search_cv_profiles, delete_cv_profile, delete_cv_profile_by_id
)
from collections import Counter
import json


def get_role_redirect(user):
    """Get redirect URL based on user role."""
    if user.is_student():
        return redirect('cv_extraction:student_dashboard')
    elif user.is_company():
        return redirect('cv_extraction:company_dashboard')
    elif user.is_admin():
        return redirect('cv_extraction:admin_dashboard')
    return redirect('cv_extraction:home')


@login_required
def home(request):
    """Home page - redirects based on role."""
    return get_role_redirect(request.user)


@login_required
def student_dashboard(request):
    """Student dashboard with CV upload and profile view."""
    if not request.user.is_student():
        messages.error(request, 'Access denied. Student access only.')
        return redirect('cv_extraction:home')
    
    # Get student's CV profile
    cv_profile = get_cv_profile(request.user.id)
    
    # Calculate profile completeness
    completeness = 0
    total_fields = 8
    if cv_profile:
        if cv_profile.get('full_name'): completeness += 1
        if cv_profile.get('email'): completeness += 1
        if cv_profile.get('phone'): completeness += 1
        if cv_profile.get('summary'): completeness += 1
        if cv_profile.get('major'): completeness += 1
        if cv_profile.get('gpa'): completeness += 1
        if cv_profile.get('skills') and len(cv_profile.get('skills', [])) > 0: completeness += 1
        if cv_profile.get('experience') and len(cv_profile.get('experience', [])) > 0: completeness += 1
    
    profile_completeness = round((completeness / total_fields) * 100) if total_fields > 0 else 0
    
    context = {
        'cv_profile': cv_profile,
        'user': request.user,
        'profile_completeness': profile_completeness,
    }
    
    return render(request, 'cv_extraction/student_dashboard.html', context)


@login_required
def upload_cv(request):
    """CV upload view for students."""
    if not request.user.is_student():
        messages.error(request, 'Access denied. Student access only.')
        return redirect('cv_extraction:home')
    
    if request.method == 'POST':
        form = CVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                cv_file = request.FILES['cv_file']
                file_content = cv_file.read()
                
                # Extract CV data using Cohere
                extractor = CVExtractor()
                cv_data = extractor.process_cv_file(file_content, cv_file.name)
                
                # Convert Pydantic model to dict
                cv_dict = cv_data.model_dump()
                
                # Save to MongoDB
                save_cv_profile(request.user.id, cv_dict)
                
                # Store extracted data in session to show on next page
                request.session['extracted_cv_data'] = cv_dict
                request.session['cv_filename'] = cv_file.name
                
                messages.success(request, 'CV uploaded and processed successfully!')
                return redirect('cv_extraction:show_extracted_data')
                
            except Exception as e:
                messages.error(request, f'Error processing CV: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = CVUploadForm()
    
    return render(request, 'cv_extraction/upload_cv.html', {'form': form})


@login_required
def edit_cv_profile(request):
    """Edit CV profile data."""
    if not request.user.is_student():
        messages.error(request, 'Access denied. Student access only.')
        return redirect('cv_extraction:home')
    
    # Get current CV profile
    cv_profile = get_cv_profile(request.user.id)
    
    if not cv_profile:
        messages.error(request, 'No CV profile found. Please upload a CV first.')
        return redirect('cv_extraction:upload_cv')
    
    if request.method == 'POST':
        form = CVProfileEditForm(request.POST)
        if form.is_valid():
            try:
                # Prepare data for MongoDB
                cv_data = {
                    'full_name': form.cleaned_data.get('full_name', ''),
                    'email': form.cleaned_data.get('email', ''),
                    'phone': form.cleaned_data.get('phone', ''),
                    'summary': form.cleaned_data.get('summary', ''),
                    'major': form.cleaned_data.get('major', ''),
                    'gpa': form.cleaned_data.get('gpa'),
                    'skills': form.cleaned_data.get('skills', []),
                    'education': form.cleaned_data.get('education', []),
                    'experience': form.cleaned_data.get('experience', []),
                    'certifications': form.cleaned_data.get('certifications', []),
                    'languages': form.cleaned_data.get('languages', []),
                }
                
                # Update in MongoDB
                save_cv_profile(request.user.id, cv_data)
                
                messages.success(request, 'CV profile updated successfully!')
                return redirect('cv_extraction:student_dashboard')
                
            except Exception as e:
                messages.error(request, f'Error updating profile: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        # Pre-populate form with existing data
        initial_data = {
            'full_name': cv_profile.get('full_name', ''),
            'email': cv_profile.get('email', ''),
            'phone': cv_profile.get('phone', ''),
            'summary': cv_profile.get('summary', ''),
            'major': cv_profile.get('major', ''),
            'gpa': cv_profile.get('gpa'),
            'skills': ', '.join(cv_profile.get('skills', [])),
            'education': '\n'.join(cv_profile.get('education', [])),
            'experience': '\n'.join(cv_profile.get('experience', [])),
            'certifications': '\n'.join(cv_profile.get('certifications', [])),
            'languages': ', '.join(cv_profile.get('languages', [])),
        }
        form = CVProfileEditForm(initial=initial_data)
    
    return render(request, 'cv_extraction/edit_cv_profile.html', {
        'form': form,
        'cv_profile': cv_profile,
    })


@login_required
def show_extracted_data(request):
    """Show extracted CV data after upload."""
    if not request.user.is_student():
        messages.error(request, 'Access denied. Student access only.')
        return redirect('cv_extraction:home')
    
    # Get extracted data from session
    extracted_data = request.session.get('extracted_cv_data')
    cv_filename = request.session.get('cv_filename')
    
    if not extracted_data:
        messages.info(request, 'No extracted data found. Please upload a CV first.')
        return redirect('cv_extraction:upload_cv')
    
    # Clear session data after showing
    del request.session['extracted_cv_data']
    if 'cv_filename' in request.session:
        del request.session['cv_filename']
    
    context = {
        'extracted_data': extracted_data,
        'cv_filename': cv_filename,
    }
    
    return render(request, 'cv_extraction/show_extracted_data.html', context)


@login_required
def student_browse(request):
    """Browse other students' profiles."""
    if not request.user.is_student():
        messages.error(request, 'Access denied. Student access only.')
        return redirect('cv_extraction:home')
    
    # Get all CV profiles
    all_profiles = get_all_cv_profiles()
    
    # Filter and normalize user_ids, exclude current user
    student_profiles = []
    for p in all_profiles:
        user_id = p.get('user_id')
        # Convert to int if it's a string or ensure it's an int
        try:
            if user_id:
                user_id = int(user_id)
                # Exclude current user's profile
                if user_id != request.user.id:
                    p['user_id'] = user_id
                    student_profiles.append(p)
        except (ValueError, TypeError):
            # Skip profiles with invalid user_ids
            continue
    
    # Get user info for all profiles (not just students)
    user_ids = [p.get('user_id') for p in student_profiles if p.get('user_id')]
    if user_ids:
        # Get all users (not filtered by role yet)
        all_users = {user.id: user for user in User.objects.filter(id__in=user_ids)}
        # Separate students from others
        student_users = {uid: user for uid, user in all_users.items() if user.role == 'student'}
    else:
        all_users = {}
        student_users = {}
    
    # Add user info to profiles - show all profiles but mark which are students
    valid_profiles = []
    for profile in student_profiles:
        user_id = profile.get('user_id')
        if user_id:
            # Add user if exists
            if user_id in all_users:
                profile['user'] = all_users[user_id]
                profile['is_student'] = user_id in student_users
            else:
                profile['user'] = None
                profile['is_student'] = False
            valid_profiles.append(profile)
    
    context = {
        'profiles': valid_profiles,
        'total_count': len(valid_profiles),
    }
    
    return render(request, 'cv_extraction/student_browse.html', context)


@login_required
def student_profile(request, user_id=None):
    """View student profile (public data)."""
    profile_user_id = user_id if user_id else request.user.id
    
    # Convert to int if it's a string
    try:
        profile_user_id = int(profile_user_id)
    except (ValueError, TypeError):
        messages.error(request, 'Invalid user ID.')
        return redirect('cv_extraction:home')
    
    # Students can view their own profile or other students' profiles
    if request.user.is_student() and profile_user_id != request.user.id:
        # Students can view other students' profiles
        pass
    elif request.user.is_student() and profile_user_id == request.user.id:
        # Own profile
        pass
    elif not (request.user.is_company() or request.user.is_admin() or request.user.is_student()):
        messages.error(request, 'Access denied.')
        return redirect('cv_extraction:home')
    
    # First check if CV profile exists
    cv_profile = get_cv_profile(profile_user_id)
    if not cv_profile:
        messages.error(request, 'CV profile not found.')
        return redirect('cv_extraction:home')
    
    # Get user info - handle case where user might not exist
    try:
        profile_user = User.objects.get(id=profile_user_id)
    except User.DoesNotExist:
        # If CV profile exists but user doesn't, show profile with limited info
        # This can happen if user was deleted but CV profile remains
        messages.warning(request, 'User account not found, but showing CV profile information.')
        profile_user = None
    
    context = {
        'cv_profile': cv_profile,
        'profile_user': profile_user,
        'is_own_profile': profile_user_id == request.user.id,
    }
    
    return render(request, 'cv_extraction/student_profile.html', context)


@login_required
def company_dashboard(request):
    """Company dashboard with student list and filters."""
    if not request.user.is_company():
        messages.error(request, 'Access denied. Company access only.')
        return redirect('cv_extraction:home')
    
    # Get all CV profiles
    all_profiles = get_all_cv_profiles()
    
    # Normalize and filter user_ids
    valid_user_ids = []
    for profile in all_profiles:
        user_id = profile.get('user_id')
        try:
            if user_id:
                user_id = int(user_id)
                profile['user_id'] = user_id
                valid_user_ids.append(user_id)
        except (ValueError, TypeError):
            # Skip profiles with invalid user_ids
            continue
    
    # Get user info for each profile
    if valid_user_ids:
        users = {user.id: user for user in User.objects.filter(id__in=valid_user_ids)}
    else:
        users = {}
    
    # Add user info to profiles and filter out invalid ones
    valid_profiles = []
    for profile in all_profiles:
        user_id = profile.get('user_id')
        if user_id and user_id in users:
            profile['user'] = users.get(user_id)
            valid_profiles.append(profile)
    
    all_profiles = valid_profiles
    
    # Apply filters
    form = StudentFilterForm(request.GET)
    if form.is_valid():
        filtered_profiles = all_profiles.copy()
        
        # GPA filter
        gpa_min = form.cleaned_data.get('gpa_min')
        gpa_max = form.cleaned_data.get('gpa_max')
        if gpa_min is not None:
            filtered_profiles = [
                p for p in filtered_profiles
                if p.get('gpa') is not None and p.get('gpa') >= gpa_min
            ]
        if gpa_max is not None:
            filtered_profiles = [
                p for p in filtered_profiles
                if p.get('gpa') is not None and p.get('gpa') <= gpa_max
            ]
        
        # Major filter
        major = form.cleaned_data.get('major')
        if major:
            filtered_profiles = [
                p for p in filtered_profiles
                if major.lower() in (p.get('major') or '').lower()
            ]
        
        # Skills filter
        skills = form.cleaned_data.get('skills')
        if skills:
            skill_list = [s.strip().lower() for s in skills.split(',')]
            filtered_profiles = [
                p for p in filtered_profiles
                if any(skill in [sk.lower() for sk in p.get('skills', [])] for skill in skill_list)
            ]
        
        # Search filter
        search = form.cleaned_data.get('search')
        if search:
            search_lower = search.lower()
            filtered_profiles = [
                p for p in filtered_profiles
                if (search_lower in (p.get('full_name') or '').lower() or
                    search_lower in (p.get('email') or '').lower() or
                    search_lower in (p.get('summary') or '').lower())
            ]
        
        all_profiles = filtered_profiles
    
    context = {
        'profiles': all_profiles,
        'form': form,
        'total_count': len(all_profiles),
    }
    
    return render(request, 'cv_extraction/company_dashboard.html', context)


@login_required
def compare_students(request):
    """Student comparison page."""
    if not request.user.is_company():
        messages.error(request, 'Access denied. Company access only.')
        return redirect('cv_extraction:home')
    
    all_profiles = get_all_cv_profiles()
    
    # Normalize and filter user_ids - only include profiles with valid users
    valid_profiles = []
    valid_user_ids = []
    for profile in all_profiles:
        user_id = profile.get('user_id')
        try:
            if user_id:
                user_id = int(user_id)
                profile['user_id'] = user_id
                valid_user_ids.append(user_id)
                valid_profiles.append(profile)
        except (ValueError, TypeError):
            continue
    
    # Get user info
    if valid_user_ids:
        users = {user.id: user for user in User.objects.filter(id__in=valid_user_ids)}
        for profile in valid_profiles:
            profile['user'] = users.get(profile.get('user_id'))
    
    all_profiles = valid_profiles
    
    if request.method == 'POST':
        form = StudentComparisonForm(request.POST, students=all_profiles)
        if form.is_valid():
            student_ids = [int(sid) for sid in form.cleaned_data['student_ids']]
            selected_profiles = [
                p for p in all_profiles
                if p.get('user_id') in student_ids
            ]
            
            # Get user info
            users = {user.id: user for user in User.objects.filter(id__in=student_ids)}
            for profile in selected_profiles:
                profile['user'] = users.get(profile.get('user_id'))
            
            # Calculate comparison metrics
            comparison_data = []
            for profile in selected_profiles:
                comparison_data.append({
                    'profile': profile,
                    'gpa': profile.get('gpa', 0) or 0,
                    'skills_count': len(profile.get('skills', [])),
                    'experience_count': len(profile.get('experience', [])),
                    'education_count': len(profile.get('education', [])),
                    'certifications_count': len(profile.get('certifications', [])),
                })
            
            # Find strongest candidate
            if comparison_data:
                # Score based on GPA (40%), skills (30%), experience (20%), certifications (10%)
                for data in comparison_data:
                    score = (
                        (data['gpa'] / 4.0) * 40 +
                        min(data['skills_count'] / 20, 1) * 30 +
                        min(data['experience_count'] / 10, 1) * 20 +
                        min(data['certifications_count'] / 5, 1) * 10
                    )
                    data['score'] = score
                
                comparison_data.sort(key=lambda x: x['score'], reverse=True)
                comparison_data[0]['is_strongest'] = True
            
            context = {
                'comparison_data': comparison_data,
                'form': StudentComparisonForm(students=all_profiles),
            }
            return render(request, 'cv_extraction/compare_students.html', context)
    else:
        form = StudentComparisonForm(students=all_profiles)
    
    context = {
        'form': form,
        'profiles': all_profiles,
    }
    
    return render(request, 'cv_extraction/compare_students.html', context)


@login_required
def admin_dashboard(request):
    """Admin dashboard with analytics."""
    if not request.user.is_admin():
        messages.error(request, 'Access denied. Admin access only.')
        return redirect('cv_extraction:home')
    
    # Get all data
    all_profiles = get_all_cv_profiles()
    all_users = User.objects.all()
    
    # Calculate analytics
    total_students = all_users.filter(role='student').count()
    total_companies = all_users.filter(role='company').count()
    
    # Most common skills
    all_skills = []
    for profile in all_profiles:
        all_skills.extend(profile.get('skills', []))
    skill_counts = Counter(all_skills)
    most_common_skills = skill_counts.most_common(10)
    
    # Majors distribution
    majors = [p.get('major') for p in all_profiles if p.get('major')]
    major_counts = Counter(majors)
    majors_distribution = dict(major_counts.most_common(10))
    
    # Average GPA
    gpas = [p.get('gpa') for p in all_profiles if p.get('gpa') is not None]
    avg_gpa = sum(gpas) / len(gpas) if gpas else 0
    
    # Prepare chart data
    from django.utils.safestring import mark_safe
    import json
    
    # Users distribution for pie chart
    users_distribution = {
        'labels': json.dumps(['Students', 'Companies', 'Admins']),
        'data': json.dumps([
            total_students,
            total_companies,
            all_users.filter(role='admin').count()
        ])
    }
    
    # Skills data for bar chart (top 8)
    skills_labels = [skill[0] for skill in most_common_skills[:8]]
    skills_data = [skill[1] for skill in most_common_skills[:8]]
    skills_chart_data = {
        'labels': json.dumps(skills_labels),
        'data': json.dumps(skills_data)
    }
    
    # Majors data for pie chart (top 8)
    majors_list = list(majors_distribution.items())[:8]
    majors_labels = [m[0] if m[0] else 'Not specified' for m in majors_list]
    majors_data = [m[1] for m in majors_list]
    majors_chart_data = {
        'labels': json.dumps(majors_labels),
        'data': json.dumps(majors_data)
    }
    
    # GPA distribution (bins)
    gpa_bins = {'0-2.0': 0, '2.0-2.5': 0, '2.5-3.0': 0, '3.0-3.5': 0, '3.5-4.0': 0}
    for gpa in gpas:
        if gpa < 2.0:
            gpa_bins['0-2.0'] += 1
        elif gpa < 2.5:
            gpa_bins['2.0-2.5'] += 1
        elif gpa < 3.0:
            gpa_bins['2.5-3.0'] += 1
        elif gpa < 3.5:
            gpa_bins['3.0-3.5'] += 1
        else:
            gpa_bins['3.5-4.0'] += 1
    
    gpa_distribution = {
        'labels': json.dumps(list(gpa_bins.keys())),
        'data': json.dumps(list(gpa_bins.values()))
    }
    
    context = {
        'total_students': total_students,
        'total_companies': total_companies,
        'total_profiles': len(all_profiles),
        'most_common_skills': most_common_skills,
        'majors_distribution': majors_distribution,
        'avg_gpa': round(avg_gpa, 2),
        'users_distribution': users_distribution,
        'skills_chart_data': skills_chart_data,
        'majors_chart_data': majors_chart_data,
        'gpa_distribution': gpa_distribution,
    }
    
    return render(request, 'cv_extraction/admin_dashboard.html', context)


@login_required
def admin_delete_user(request, user_id):
    """Admin delete user."""
    if not request.user.is_admin():
        messages.error(request, 'Access denied. Admin access only.')
        return redirect('cv_extraction:home')
    
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        # Delete CV profile if exists
        delete_cv_profile(user_id)
        # Delete user
        user.delete()
        messages.success(request, f'User {user.username} deleted successfully.')
        return redirect('cv_extraction:admin_dashboard')
    
    return render(request, 'cv_extraction/admin_delete_user.html', {'target_user': user})


@login_required
def admin_delete_cv(request, user_id):
    """Admin delete CV profile."""
    if not request.user.is_admin():
        messages.error(request, 'Access denied. Admin access only.')
        return redirect('cv_extraction:home')
    
    if request.method == 'POST':
        success = delete_cv_profile(user_id)
        if success:
            messages.success(request, 'CV profile deleted successfully.')
        else:
            messages.error(request, 'CV profile not found.')
        return redirect('cv_extraction:admin_user_detail', user_id=user_id)
    
    return redirect('cv_extraction:admin_user_detail', user_id=user_id)


@login_required
def admin_users(request):
    """Admin view all users."""
    if not request.user.is_admin():
        messages.error(request, 'Access denied. Admin access only.')
        return redirect('cv_extraction:home')
    
    all_users = User.objects.all().order_by('-date_joined')
    
    # Get CV profile status for each user
    all_profiles = get_all_cv_profiles()
    profile_user_ids = {p.get('user_id') for p in all_profiles}
    
    for user in all_users:
        user.has_cv_profile = user.id in profile_user_ids
    
    context = {
        'users': all_users,
    }
    
    return render(request, 'cv_extraction/admin_users.html', context)


@login_required
def admin_user_detail(request, user_id):
    """Admin view user details."""
    if not request.user.is_admin():
        messages.error(request, 'Access denied. Admin access only.')
        return redirect('cv_extraction:home')
    
    user = get_object_or_404(User, id=user_id)
    cv_profile = get_cv_profile(user_id)
    
    context = {
        'target_user': user,
        'cv_profile': cv_profile,
    }
    
    return render(request, 'cv_extraction/admin_user_detail.html', context)


@login_required
def admin_edit_user(request, user_id):
    """Admin edit user - can update all user information including username and password."""
    if not request.user.is_admin():
        messages.error(request, 'Access denied. Admin access only.')
        return redirect('cv_extraction:home')
    
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        # Update username if provided and different
        new_username = request.POST.get('username', '').strip()
        if new_username and new_username != user.username:
            # Check if username already exists
            if User.objects.filter(username=new_username).exclude(id=user_id).exists():
                messages.error(request, f'Username "{new_username}" is already taken.')
                return redirect('cv_extraction:admin_edit_user', user_id=user_id)
            user.username = new_username
        
        # Update other user fields
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.role = request.POST.get('role', user.role)
        user.is_active = request.POST.get('is_active') == 'on'
        
        # Update password if provided
        new_password = request.POST.get('password', '').strip()
        if new_password:
            user.set_password(new_password)
        
        user.save()
        
        messages.success(request, f'User {user.username} updated successfully.')
        return redirect('cv_extraction:admin_user_detail', user_id=user_id)
    
    context = {
        'target_user': user,
    }
    
    return render(request, 'cv_extraction/admin_edit_user.html', context)


@login_required
def admin_edit_cv_profile(request, user_id):
    """Admin edit CV profile - can update all CV information."""
    if not request.user.is_admin():
        messages.error(request, 'Access denied. Admin access only.')
        return redirect('cv_extraction:home')
    
    user = get_object_or_404(User, id=user_id)
    cv_profile = get_cv_profile(user_id)
    
    if request.method == 'POST':
        # Get all CV data from form
        cv_data = {
            'full_name': request.POST.get('full_name', ''),
            'email': request.POST.get('email', ''),
            'phone': request.POST.get('phone', ''),
            'summary': request.POST.get('summary', ''),
            'major': request.POST.get('major', ''),
            'gpa': request.POST.get('gpa', '') or None,
            'skills': [s.strip() for s in request.POST.get('skills', '').split(',') if s.strip()],
            'education': [e.strip() for e in request.POST.get('education', '').split('\n') if e.strip()],
            'experience': [exp.strip().lstrip('- ').strip() for exp in request.POST.get('experience', '').split('\n') if exp.strip()],
            'certifications': [c.strip() for c in request.POST.get('certifications', '').split('\n') if c.strip()],
            'languages': [l.strip() for l in request.POST.get('languages', '').split(',') if l.strip()],
        }
        
        # Convert GPA to float if provided
        if cv_data['gpa']:
            try:
                cv_data['gpa'] = float(cv_data['gpa'])
            except ValueError:
                cv_data['gpa'] = None
        
        # Save CV profile
        save_cv_profile(user_id, cv_data)
        
        messages.success(request, f'CV profile for {user.username} updated successfully.')
        return redirect('cv_extraction:admin_user_detail', user_id=user_id)
    
    context = {
        'target_user': user,
        'cv_profile': cv_profile or {},
    }
    
    return render(request, 'cv_extraction/admin_edit_cv_profile.html', context)

