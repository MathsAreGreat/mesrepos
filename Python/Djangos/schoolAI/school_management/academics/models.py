from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Class(models.Model):
    """Model representing a school class/grade level"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Classes"


class Subject(models.Model):
    """Model representing a school subject"""
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    credits = models.PositiveIntegerField(default=1)
    classes = models.ManyToManyField(Class, related_name='subjects', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Teacher(models.Model):
    """Model representing a teacher"""
    employee_id = models.CharField(max_length=20, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    hire_date = models.DateField(default=timezone.now)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='teachers', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"

    @property
    def full_name(self):
        return self.user.get_full_name()

    @property
    def email(self):
        return self.user.email


class Student(models.Model):
    """Model representing a student"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    student_id = models.CharField(max_length=20, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    parent_name = models.CharField(max_length=100, blank=True)
    parent_phone = models.CharField(max_length=15, blank=True)
    parent_email = models.EmailField(blank=True)
    enrollment_date = models.DateField(default=timezone.now)
    current_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.student_id})"

    @property
    def full_name(self):
        return self.user.get_full_name()

    @property
    def email(self):
        return self.user.email

    @property
    def age(self):
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )


class ClassSubject(models.Model):
    """Model representing which subjects are taught in which classes"""
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='class_subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='class_subjects')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teaching_assignments')
    academic_year = models.CharField(max_length=9)  # e.g., "2023-2024"
    semester = models.CharField(max_length=20, default="First Semester")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['class_obj', 'subject', 'academic_year', 'semester']
        verbose_name_plural = "Class Subjects"

    def __str__(self):
        return f"{self.class_obj.name} - {self.subject.name} ({self.academic_year})"


class Mark(models.Model):
    """Model representing student marks for subjects"""
    MARK_TYPES = [
        ('assignment', 'Assignment'),
        ('quiz', 'Quiz'),
        ('midterm', 'Midterm'),
        ('final', 'Final'),
        ('project', 'Project'),
        ('participation', 'Participation'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    class_subject = models.ForeignKey(ClassSubject, on_delete=models.CASCADE, related_name='marks')
    mark_type = models.CharField(max_length=20, choices=MARK_TYPES)
    score = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    remarks = models.TextField(blank=True)
    date_given = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'class_subject', 'mark_type', 'date_given']

    def __str__(self):
        return f"{self.student.full_name} - {self.class_subject.subject.name} - {self.mark_type}"

    @property
    def percentage(self):
        """Calculate the percentage score"""
        if self.max_score > 0:
            return (self.score / self.max_score) * 100
        return 0

    @property
    def grade(self):
        """Calculate letter grade based on percentage"""
        percentage = self.percentage
        if percentage >= 90:
            return 'A+'
        elif percentage >= 85:
            return 'A'
        elif percentage >= 80:
            return 'A-'
        elif percentage >= 75:
            return 'B+'
        elif percentage >= 70:
            return 'B'
        elif percentage >= 65:
            return 'B-'
        elif percentage >= 60:
            return 'C+'
        elif percentage >= 55:
            return 'C'
        elif percentage >= 50:
            return 'C-'
        elif percentage >= 45:
            return 'D+'
        elif percentage >= 40:
            return 'D'
        else:
            return 'F'


class Attendance(models.Model):
    """Model representing student attendance"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    class_subject = models.ForeignKey(ClassSubject, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    is_present = models.BooleanField(default=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'class_subject', 'date']

    def __str__(self):
        status = "Present" if self.is_present else "Absent"
        return f"{self.student.full_name} - {self.class_subject.subject.name} - {self.date} - {status}"
