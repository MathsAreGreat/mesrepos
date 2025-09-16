from django.contrib import admin
from django.utils.html import format_html
from .models import Class, Subject, Teacher, Student, ClassSubject, Mark, Attendance


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'student_count', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']
    ordering = ['name']

    def student_count(self, obj):
        return obj.students.count()
    student_count.short_description = 'Number of Students'


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'credits', 'classes_display', 'is_active', 'teacher_count', 'created_at']
    search_fields = ['name', 'code', 'description']
    list_filter = ['is_active', 'credits', 'created_at']
    ordering = ['name']
    filter_horizontal = ['classes']

    def classes_display(self, obj):
        return ', '.join([c.name for c in obj.classes.all()[:3]])
    classes_display.short_description = 'Classes'

    def teacher_count(self, obj):
        return obj.teachers.count()
    teacher_count.short_description = 'Number of Teachers'


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'employee_id', 'email', 'phone', 'hire_date', 'is_active', 'subject']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'employee_id', 'phone']
    list_filter = ['is_active', 'hire_date', 'subject', 'created_at']
    ordering = ['user__first_name', 'user__last_name']

    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Full Name'

    def email(self, obj):
        return obj.email
    email.short_description = 'Email'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'student_id', 'current_class', 'age', 'gender', 'enrollment_date', 'is_active']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'student_id', 'parent_name']
    list_filter = ['is_active', 'gender', 'current_class', 'enrollment_date', 'created_at']
    ordering = ['user__first_name', 'user__last_name']
    readonly_fields = ['age']

    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Full Name'

    def age(self, obj):
        return obj.age
    age.short_description = 'Age'


@admin.register(ClassSubject)
class ClassSubjectAdmin(admin.ModelAdmin):
    list_display = ['class_obj', 'subject', 'teacher', 'academic_year', 'semester', 'is_active']
    search_fields = ['class_obj__name', 'subject__name', 'teacher__user__first_name', 'teacher__user__last_name']
    list_filter = ['is_active', 'academic_year', 'semester', 'class_obj', 'subject']
    ordering = ['academic_year', 'class_obj__name', 'subject__name']


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'mark_type', 'score', 'max_score', 'percentage', 'grade', 'date_given']
    search_fields = ['student__user__first_name', 'student__user__last_name', 'class_subject__subject__name']
    list_filter = ['mark_type', 'date_given', 'class_subject__subject', 'class_subject__class_obj']
    ordering = ['-date_given', 'student__user__first_name']
    readonly_fields = ['percentage', 'grade']

    def subject(self, obj):
        return obj.class_subject.subject.name
    subject.short_description = 'Subject'

    def percentage(self, obj):
        return f"{obj.percentage:.1f}%"
    percentage.short_description = 'Percentage'

    def grade(self, obj):
        return format_html('<span style="color: {};">{}</span>', 
                          'green' if obj.grade in ['A+', 'A', 'A-'] else 
                          'orange' if obj.grade in ['B+', 'B', 'B-'] else 
                          'red' if obj.grade == 'F' else 'black', 
                          obj.grade)
    grade.short_description = 'Grade'


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'class_name', 'date', 'status', 'remarks']
    search_fields = ['student__user__first_name', 'student__user__last_name', 'class_subject__subject__name']
    list_filter = ['is_present', 'date', 'class_subject__subject', 'class_subject__class_obj']
    ordering = ['-date', 'student__user__first_name']

    def subject(self, obj):
        return obj.class_subject.subject.name
    subject.short_description = 'Subject'

    def class_name(self, obj):
        return obj.class_subject.class_obj.name
    class_name.short_description = 'Class'

    def status(self, obj):
        return format_html('<span style="color: {};">{}</span>', 
                          'green' if obj.is_present else 'red',
                          'Present' if obj.is_present else 'Absent')
    status.short_description = 'Status'
