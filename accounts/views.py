"""
Views for authentication and role-based redirects.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import UserRegistrationForm, UserProfileEditForm
from .mixins import get_role_redirect_url


def register_view(request):
    """User registration view."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            # Redirect based on role
            redirect_url = get_role_redirect_url(user)
            return redirect(redirect_url)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


class CustomLoginView(LoginView):
    """Custom login view with role-based redirect."""
    template_name = 'accounts/login.html'
    
    def get_success_url(self):
        """Redirect based on user role after login."""
        from django.urls import reverse
        return reverse(get_role_redirect_url(self.request.user))


@login_required
def profile_view(request):
    """User profile view."""
    return render(request, 'accounts/profile.html', {'user': request.user})


@login_required
def edit_profile(request):
    """Edit user personal information."""
    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = UserProfileEditForm(instance=request.user)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})

