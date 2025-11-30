"""
Forms for authentication and registration.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    """Registration form with role selection."""
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        required=True,
        help_text='Select your role'
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove admin role from choices for regular registration
        self.fields['role'].choices = [
            choice for choice in User.ROLE_CHOICES if choice[0] != 'admin'
        ]
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user


class UserProfileEditForm(forms.ModelForm):
    """Form for editing user personal information."""
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make username read-only
        if self.instance and self.instance.pk:
            self.fields['username'].widget.attrs['readonly'] = True
            self.fields['username'].help_text = 'Username cannot be changed'
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.instance and self.instance.pk:
            # If editing existing user, don't allow username change
            if username != self.instance.username:
                raise forms.ValidationError("Username cannot be changed")
        return username

