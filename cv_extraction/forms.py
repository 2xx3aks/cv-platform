"""
Forms for CV extraction app.
"""
from django import forms


class CVUploadForm(forms.Form):
    """Form for CV file upload."""
    cv_file = forms.FileField(
        label='Upload CV',
        help_text='Upload PDF or DOCX file (max 10MB)',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.docx,.doc'
        })
    )
    
    def clean_cv_file(self):
        file = self.cleaned_data.get('cv_file')
        if file:
            # Check file size (10MB max)
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError("File size must be less than 10MB")
            
            # Check file extension
            filename = file.name.lower()
            if not (filename.endswith('.pdf') or filename.endswith('.docx') or filename.endswith('.doc')):
                raise forms.ValidationError("Only PDF and DOCX files are allowed")
        
        return file


class StudentFilterForm(forms.Form):
    """Form for filtering students."""
    gpa_min = forms.FloatField(
        required=False,
        label='Min GPA',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'min': '0',
            'max': '4.0'
        })
    )
    gpa_max = forms.FloatField(
        required=False,
        label='Max GPA',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'min': '0',
            'max': '4.0'
        })
    )
    major = forms.CharField(
        required=False,
        label='Major',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Computer Science'
        })
    )
    skills = forms.CharField(
        required=False,
        label='Skills (comma-separated)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Python, JavaScript, Django'
        })
    )
    search = forms.CharField(
        required=False,
        label='Search',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, email, or summary'
        })
    )


class StudentComparisonForm(forms.Form):
    """Form for selecting students to compare."""
    student_ids = forms.MultipleChoiceField(
        label='Select Students to Compare',
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        help_text='Select 2 or more students to compare'
    )
    
    def __init__(self, *args, students=None, **kwargs):
        super().__init__(*args, **kwargs)
        if students:
            self.fields['student_ids'].choices = [
                (str(profile.get('user_id', '')), 
                 f"{profile.get('full_name', 'Unknown')} - {profile.get('major', 'N/A')} (GPA: {profile.get('gpa', 'N/A')})")
                for profile in students
            ]
    
    def clean_student_ids(self):
        student_ids = self.cleaned_data.get('student_ids')
        if len(student_ids) < 2:
            raise forms.ValidationError("Please select at least 2 students to compare")
        return student_ids


class CVProfileEditForm(forms.Form):
    """Form for editing CV profile data."""
    full_name = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Full Name'
        })
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    phone = forms.CharField(
        required=False,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone Number'
        })
    )
    summary = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Professional Summary'
        })
    )
    major = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Major/Field of Study'
        })
    )
    gpa = forms.FloatField(
        required=False,
        min_value=0.0,
        max_value=4.0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'placeholder': 'GPA (0.0 - 4.0)'
        })
    )
    skills = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Enter skills separated by commas (e.g., Python, JavaScript, Django)'
        }),
        help_text='Separate skills with commas'
    )
    education = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Enter each education entry on a new line'
        }),
        help_text='Enter each education entry on a new line'
    )
    experience = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Enter each experience entry on a new line'
        }),
        help_text='Enter each experience entry on a new line'
    )
    certifications = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Enter each certification on a new line'
        }),
        help_text='Enter each certification on a new line'
    )
    languages = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter languages separated by commas (e.g., English, Arabic)'
        }),
        help_text='Separate languages with commas'
    )
    
    def clean_skills(self):
        """Convert comma-separated skills to list."""
        skills_str = self.cleaned_data.get('skills', '')
        if skills_str:
            return [skill.strip() for skill in skills_str.split(',') if skill.strip()]
        return []
    
    def clean_education(self):
        """Convert newline-separated education to list."""
        education_str = self.cleaned_data.get('education', '')
        if education_str:
            return [edu.strip() for edu in education_str.split('\n') if edu.strip()]
        return []
    
    def clean_experience(self):
        """Convert newline-separated experience to list, removing leading dashes."""
        experience_str = self.cleaned_data.get('experience', '')
        if experience_str:
            # Remove leading dashes and whitespace from each line
            return [exp.strip().lstrip('- ').strip() for exp in experience_str.split('\n') if exp.strip()]
        return []
    
    def clean_certifications(self):
        """Convert newline-separated certifications to list."""
        certs_str = self.cleaned_data.get('certifications', '')
        if certs_str:
            return [cert.strip() for cert in certs_str.split('\n') if cert.strip()]
        return []
    
    def clean_languages(self):
        """Convert comma-separated languages to list."""
        languages_str = self.cleaned_data.get('languages', '')
        if languages_str:
            return [lang.strip() for lang in languages_str.split(',') if lang.strip()]
        return []

