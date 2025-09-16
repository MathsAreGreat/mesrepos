from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import Student, Teacher, Class, Subject


class StudentUpdateForm(forms.ModelForm):
    """Form for updating student information"""
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'student_id', 'current_class', 
                 'date_of_birth', 'gender', 'phone', 'address', 
                 'parent_name', 'parent_phone', 'parent_email', 'is_active']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'text', 'placeholder': 'dd/mm/YYYY'}, format='%d/%m/%Y'),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
        # Add Bootstrap classes to all form fields
        for field_name, field in self.fields.items():
            if field_name != 'is_active':
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({'class': 'form-check-input'})
        self.fields['date_of_birth'].input_formats = ['%d/%m/%Y']
    
    def save(self, commit=True):
        student = super().save(commit=False)
        if commit:
            # Update user information
            if student.user:
                student.user.first_name = self.cleaned_data['first_name']
                student.user.last_name = self.cleaned_data['last_name']
                student.user.email = self.cleaned_data['email']
                student.user.save()
            student.save()
        return student


class TeacherUpdateForm(forms.ModelForm):
    """Form for updating teacher information"""
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'email', 'employee_id', 'phone', 
                 'address', 'date_of_birth', 'hire_date', 'subject', 'is_active']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'text', 'placeholder': 'dd/mm/YYYY'}, format='%d/%m/%Y'),
            'hire_date': forms.DateInput(attrs={'type': 'text', 'placeholder': 'dd/mm/YYYY'}, format='%d/%m/%Y'),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
        # Add Bootstrap classes to all form fields
        for field_name, field in self.fields.items():
            if field_name != 'is_active':
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({'class': 'form-check-input'})
        self.fields['date_of_birth'].input_formats = ['%d/%m/%Y']
        self.fields['hire_date'].input_formats = ['%d/%m/%Y']
    
    def save(self, commit=True):
        teacher = super().save(commit=False)
        if commit:
            # Update user information
            if teacher.user:
                teacher.user.first_name = self.cleaned_data['first_name']
                teacher.user.last_name = self.cleaned_data['last_name']
                teacher.user.email = self.cleaned_data['email']
                teacher.user.save()
            teacher.save()
        return teacher


class StudentCreateForm(forms.ModelForm):
    """Form for creating new students"""
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=30, required=True, help_text="Username for login")
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'student_id', 'current_class', 
                 'date_of_birth', 'gender', 'phone', 'address', 
                 'parent_name', 'parent_phone', 'parent_email']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'text', 'placeholder': 'dd/mm/YYYY'}, format='%d/%m/%Y'),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all form fields
        for field_name, field in self.fields.items():
            if field_name != 'password':
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
        self.fields['date_of_birth'].input_formats = ['%d/%m/%Y']
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
    
    def save(self, commit=True):
        student = super().save(commit=False)
        if commit:
            # Create user
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name']
            )
            student.user = user
            student.save()
        return student


class TeacherCreateForm(forms.ModelForm):
    """Form for creating new teachers"""
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=30, required=True, help_text="Username for login")
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'employee_id', 'phone', 
                 'address', 'date_of_birth', 'hire_date', 'subject']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'text', 'placeholder': 'dd/mm/YYYY'}, format='%d/%m/%Y'),
            'hire_date': forms.DateInput(attrs={'type': 'text', 'placeholder': 'dd/mm/YYYY'}, format='%d/%m/%Y'),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all form fields
        for field_name, field in self.fields.items():
            if field_name != 'password':
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
        self.fields['date_of_birth'].input_formats = ['%d/%m/%Y']
        self.fields['hire_date'].input_formats = ['%d/%m/%Y']
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
    
    def save(self, commit=True):
        teacher = super().save(commit=False)
        if commit:
            # Create user
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name']
            )
            teacher.user = user
            teacher.save()
        return teacher


class ClassCreateForm(forms.ModelForm):
    """Form for creating new classes"""
    class Meta:
        model = Class
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class SubjectCreateForm(forms.ModelForm):
    """Form for creating new subjects"""
    class Meta:
        model = Subject
        fields = ['code', 'name', 'credits', 'description']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'credits': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class CSVUploadForm(forms.Form):
    """Base form for CSV uploads"""
    csv_file = forms.FileField(
        label='CSV File',
        help_text='Upload a CSV file with the required headers',
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.csv'})
    )
    
    def clean_csv_file(self):
        csv_file = self.cleaned_data['csv_file']
        if not csv_file.name.endswith('.csv'):
            raise forms.ValidationError("Please upload a CSV file.")
        return csv_file 