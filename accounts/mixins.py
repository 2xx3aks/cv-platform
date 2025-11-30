"""
Mixins for role-based access control.
"""
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin


class RoleRequiredMixin(LoginRequiredMixin):
    """Mixin to require specific role."""
    required_role = None
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        if self.required_role and not getattr(request.user, f'is_{self.required_role}')():
            from django.contrib import messages
            messages.error(request, f'Access denied. {self.required_role.capitalize()} access only.')
            return redirect('cv_extraction:home')
        
        return super().dispatch(request, *args, **kwargs)


def get_role_redirect_url(user):
    """Get redirect URL based on user role."""
    if user.is_student():
        return 'cv_extraction:student_dashboard'
    elif user.is_company():
        return 'cv_extraction:company_dashboard'
    elif user.is_admin():
        return 'cv_extraction:admin_dashboard'
    return 'cv_extraction:home'

