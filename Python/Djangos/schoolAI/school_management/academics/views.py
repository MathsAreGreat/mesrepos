from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg, Q
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import datetime, timedelta
import csv
import io
from django.contrib.auth.models import User
from .models import Student, Teacher, Subject, Class, Mark, Attendance, ClassSubject
from .forms import StudentUpdateForm, TeacherUpdateForm, StudentCreateForm, TeacherCreateForm, ClassCreateForm, SubjectCreateForm, CSVUploadForm


@login_required
def dashboard(request):
    """Main dashboard view with statistics"""
    context = {
        'total_students': Student.objects.filter(is_active=True).count(),
        'total_teachers': Teacher.objects.filter(is_active=True).count(),
        'total_subjects': Subject.objects.filter(is_active=True).count(),
        'total_classes': Class.objects.count(),
    }
    
    # Recent activities
    recent_marks = Mark.objects.select_related('student', 'class_subject__subject').order_by('-created_at')[:5]
    recent_attendance = Attendance.objects.select_related('student', 'class_subject__subject').order_by('-date')[:5]
    
    context.update({
        'recent_marks': recent_marks,
        'recent_attendance': recent_attendance,
    })
    
    return render(request, 'academics/dashboard.html', context)


@login_required
def student_list(request):
    """List all students with search and filter functionality"""
    students = Student.objects.select_related('user', 'current_class').filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        students = students.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(student_id__icontains=search_query) |
            Q(user__email__icontains=search_query)
        )
    
    # Filter by class
    class_filter = request.GET.get('class', '')
    if class_filter:
        students = students.filter(current_class_id=class_filter)
    
    # Get all classes for filter dropdown
    classes = Class.objects.all()
    
    # Pagination
    paginator = Paginator(students, 10)  # Show 10 students per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'students': page_obj,
        'classes': classes,
        'search_query': search_query,
        'class_filter': class_filter,
        'is_paginated': paginator.num_pages > 1,
        'page_obj': page_obj,
    }
    
    return render(request, 'academics/student_list.html', context)


@login_required
def student_detail(request, student_id):
    """Detailed view of a student with marks and attendance"""
    student = get_object_or_404(Student, student_id=student_id)
    
    # Get student's marks grouped by subject
    marks = Mark.objects.filter(student=student).select_related('class_subject__subject')
    
    # Get attendance records
    attendance = Attendance.objects.filter(student=student).select_related('class_subject__subject')
    
    # Calculate attendance percentage
    total_attendance = attendance.count()
    present_count = attendance.filter(is_present=True).count()
    attendance_percentage = (present_count / total_attendance * 100) if total_attendance > 0 else 0
    
    # Get average marks by subject
    subject_averages = {}
    for mark in marks:
        subject_name = mark.class_subject.subject.name
        if subject_name not in subject_averages:
            subject_averages[subject_name] = []
        subject_averages[subject_name].append(mark.percentage)
    
    # Calculate averages
    for subject in subject_averages:
        subject_averages[subject] = sum(subject_averages[subject]) / len(subject_averages[subject])
    
    context = {
        'student': student,
        'marks': marks,
        'attendance': attendance,
        'attendance_percentage': attendance_percentage,
        'subject_averages': subject_averages,
    }
    
    return render(request, 'academics/student_detail.html', context)


@login_required
def student_update(request, student_id):
    """Update student information"""
    student = get_object_or_404(Student, student_id=student_id)
    
    if request.method == 'POST':
        form = StudentUpdateForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f'Student {student.full_name} updated successfully!')
            return redirect('academics:student_detail', student_id=student.student_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentUpdateForm(instance=student)
    
    context = {
        'form': form,
        'student': student,
        'page_title': f'Update {student.full_name}',
    }
    
    return render(request, 'academics/student_update.html', context)


@login_required
def teacher_list(request):
    """List all teachers with search functionality"""
    teachers = Teacher.objects.select_related('user').filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        teachers = teachers.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(employee_id__icontains=search_query) |
            Q(user__email__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(teachers, 10)  # Show 10 teachers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'teachers': page_obj,
        'search_query': search_query,
        'is_paginated': paginator.num_pages > 1,
        'page_obj': page_obj,
    }
    
    return render(request, 'academics/teacher_list.html', context)


@login_required
def teacher_detail(request, employee_id):
    """Detailed view of a teacher with their classes and subjects"""
    teacher = get_object_or_404(Teacher, employee_id=employee_id)
    
    # Get classes taught by this teacher
    teaching_assignments = ClassSubject.objects.filter(teacher=teacher, is_active=True).select_related('class_obj', 'subject')
    
    # Get students in teacher's classes
    students = Student.objects.filter(
        current_class__in=teaching_assignments.values_list('class_obj', flat=True),
        is_active=True
    ).select_related('user', 'current_class')
    
    context = {
        'teacher': teacher,
        'teaching_assignments': teaching_assignments,
        'students': students,
    }
    
    return render(request, 'academics/teacher_detail.html', context)


@login_required
def teacher_update(request, employee_id):
    """Update teacher information"""
    teacher = get_object_or_404(Teacher, employee_id=employee_id)
    
    if request.method == 'POST':
        form = TeacherUpdateForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, f'Teacher {teacher.full_name} updated successfully!')
            return redirect('academics:teacher_detail', employee_id=teacher.employee_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TeacherUpdateForm(instance=teacher)
    
    context = {
        'form': form,
        'teacher': teacher,
        'page_title': f'Update {teacher.full_name}',
    }
    
    return render(request, 'academics/teacher_update.html', context)


@login_required
def subject_list(request):
    """List all subjects with teacher information"""
    subjects = Subject.objects.filter(is_active=True).prefetch_related('teachers__user')
    
    # Pagination
    paginator = Paginator(subjects, 10)  # Show 10 subjects per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'subjects': page_obj,
        'is_paginated': paginator.num_pages > 1,
        'page_obj': page_obj,
    }
    
    return render(request, 'academics/subject_list.html', context)


@login_required
def mark_management(request):
    """View for managing student marks"""
    if request.method == 'POST':
        # Handle mark submission
        student_id = request.POST.get('student')
        class_subject_id = request.POST.get('class_subject')
        mark_type = request.POST.get('mark_type')
        score = request.POST.get('score')
        max_score = request.POST.get('max_score', 100)
        remarks = request.POST.get('remarks', '')
        
        try:
            mark = Mark.objects.create(
                student_id=student_id,
                class_subject_id=class_subject_id,
                mark_type=mark_type,
                score=score,
                max_score=max_score,
                remarks=remarks
            )
            messages.success(request, f'Mark added successfully for {mark.student.full_name}')
            return redirect('mark_management')
        except Exception as e:
            messages.error(request, f'Error adding mark: {str(e)}')
    
    # Get form data
    students = Student.objects.filter(is_active=True).select_related('user', 'current_class')
    class_subjects = ClassSubject.objects.filter(is_active=True).select_related('class_obj', 'subject', 'teacher')
    recent_marks = Mark.objects.select_related('student', 'class_subject__subject').order_by('-created_at')[:10]
    
    context = {
        'students': students,
        'class_subjects': class_subjects,
        'recent_marks': recent_marks,
        'mark_types': Mark.MARK_TYPES,
    }
    
    return render(request, 'academics/mark_management.html', context)


@login_required
def attendance_management(request):
    """View for managing student attendance"""
    if request.method == 'POST':
        # Handle attendance submission
        student_id = request.POST.get('student')
        class_subject_id = request.POST.get('class_subject')
        date = request.POST.get('date')
        is_present = request.POST.get('is_present') == 'on'
        remarks = request.POST.get('remarks', '')
        
        try:
            attendance, created = Attendance.objects.get_or_create(
                student_id=student_id,
                class_subject_id=class_subject_id,
                date=date,
                defaults={
                    'is_present': is_present,
                    'remarks': remarks
                }
            )
            
            if not created:
                attendance.is_present = is_present
                attendance.remarks = remarks
                attendance.save()
            
            status = "Present" if is_present else "Absent"
            messages.success(request, f'Attendance marked as {status} for {attendance.student.full_name}')
            return redirect('attendance_management')
        except Exception as e:
            messages.error(request, f'Error marking attendance: {str(e)}')
    
    # Get form data
    students = Student.objects.filter(is_active=True).select_related('user', 'current_class')
    class_subjects = ClassSubject.objects.filter(is_active=True).select_related('class_obj', 'subject')
    recent_attendance = Attendance.objects.select_related('student', 'class_subject__subject').order_by('-date')[:10]
    
    context = {
        'students': students,
        'class_subjects': class_subjects,
        'recent_attendance': recent_attendance,
        'today': timezone.now().date(),
    }
    
    return render(request, 'academics/attendance_management.html', context)


@login_required
def reports(request):
    """Generate various reports"""
    # Class performance report
    class_performance = {}
    classes = Class.objects.all()
    
    for class_obj in classes:
        students = class_obj.students.filter(is_active=True)
        if students.exists():
            marks = Mark.objects.filter(student__in=students)
            if marks.exists():
                avg_score = marks.aggregate(Avg('score'))['score__avg']
                class_performance[class_obj.name] = round(avg_score, 2)
    
    # Subject performance report
    subject_performance = {}
    subjects = Subject.objects.filter(is_active=True)
    
    for subject in subjects:
        marks = Mark.objects.filter(class_subject__subject=subject)
        if marks.exists():
            avg_score = marks.aggregate(Avg('score'))['score__avg']
            subject_performance[subject.name] = round(avg_score, 2)
    
    # Attendance report
    attendance_stats = {}
    for class_obj in classes:
        students = class_obj.students.filter(is_active=True)
        if students.exists():
            attendance_records = Attendance.objects.filter(student__in=students)
            if attendance_records.exists():
                total_records = attendance_records.count()
                present_records = attendance_records.filter(is_present=True).count()
                attendance_rate = (present_records / total_records) * 100
                attendance_stats[class_obj.name] = round(attendance_rate, 2)
    
    # Calculate best class average
    best_class_average = 0
    if class_performance:
        best_class_average = max(class_performance.values())
    
    context = {
        'class_performance': class_performance,
        'subject_performance': subject_performance,
        'attendance_stats': attendance_stats,
        'best_class_average': best_class_average,
    }
    
    return render(request, 'academics/reports.html', context)


@login_required
def student_create(request):
    """Create a new student"""
    if request.method == 'POST':
        form = StudentCreateForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Student {student.full_name} created successfully!')
            return redirect('academics:student_detail', student_id=student.student_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentCreateForm()
    
    context = {
        'form': form,
        'page_title': 'Add New Student',
    }
    
    return render(request, 'academics/student_create.html', context)


@login_required
def teacher_create(request):
    """Create a new teacher"""
    if request.method == 'POST':
        form = TeacherCreateForm(request.POST)
        if form.is_valid():
            teacher = form.save()
            messages.success(request, f'Teacher {teacher.full_name} created successfully!')
            return redirect('academics:teacher_detail', employee_id=teacher.employee_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TeacherCreateForm()
    
    context = {
        'form': form,
        'page_title': 'Add New Teacher',
    }
    
    return render(request, 'academics/teacher_create.html', context)


@login_required
def class_create(request):
    """Create a new class"""
    if request.method == 'POST':
        form = ClassCreateForm(request.POST)
        if form.is_valid():
            class_obj = form.save()
            messages.success(request, f'Class {class_obj.name} created successfully!')
            return redirect('academics:class_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ClassCreateForm()
    
    context = {
        'form': form,
        'page_title': 'Add New Class',
    }
    
    return render(request, 'academics/class_create.html', context)


@login_required
def class_list(request):
    """List all classes"""
    classes = Class.objects.all()
    
    # Pagination
    paginator = Paginator(classes, 10)  # Show 10 classes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'classes': page_obj,
        'is_paginated': paginator.num_pages > 1,
        'page_obj': page_obj,
    }
    
    return render(request, 'academics/class_list.html', context)


@login_required
def class_update(request, class_id):
    """Update class information"""
    class_obj = get_object_or_404(Class, id=class_id)
    
    if request.method == 'POST':
        form = ClassCreateForm(request.POST, instance=class_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'Class {class_obj.name} updated successfully!')
            return redirect('academics:class_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ClassCreateForm(instance=class_obj)
    
    context = {
        'form': form,
        'class_obj': class_obj,
        'page_title': f'Update {class_obj.name}',
    }
    
    return render(request, 'academics/class_update.html', context)


@login_required
def class_delete(request, class_id):
    """Delete a class"""
    class_obj = get_object_or_404(Class, id=class_id)
    
    if request.method == 'POST':
        class_name = class_obj.name
        class_obj.delete()
        messages.success(request, f'Class {class_name} deleted successfully!')
        return redirect('academics:class_list')
    
    context = {
        'class_obj': class_obj,
    }
    
    return render(request, 'academics/class_confirm_delete.html', context)


@login_required
def subject_create(request):
    """Create a new subject"""
    if request.method == 'POST':
        form = SubjectCreateForm(request.POST)
        if form.is_valid():
            subject = form.save()
            messages.success(request, f'Subject {subject.name} created successfully!')
            return redirect('academics:subject_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SubjectCreateForm()
    
    context = {
        'form': form,
        'page_title': 'Add New Subject',
    }
    
    return render(request, 'academics/subject_create.html', context)


@login_required
def subject_update(request, subject_code):
    """Update subject information"""
    subject = get_object_or_404(Subject, code=subject_code)
    
    if request.method == 'POST':
        form = SubjectCreateForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, f'Subject {subject.name} updated successfully!')
            return redirect('academics:subject_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SubjectCreateForm(instance=subject)
    
    context = {
        'form': form,
        'subject': subject,
        'page_title': f'Update {subject.name}',
    }
    
    return render(request, 'academics/subject_update.html', context)


@login_required
def subject_delete(request, subject_code):
    """Delete a subject"""
    subject = get_object_or_404(Subject, code=subject_code)
    
    if request.method == 'POST':
        subject_name = subject.name
        subject.delete()
        messages.success(request, f'Subject {subject_name} deleted successfully!')
        return redirect('academics:subject_list')
    
    context = {
        'subject': subject,
    }
    
    return render(request, 'academics/subject_confirm_delete.html', context)


@login_required
def student_csv_upload(request):
    """Handle CSV upload for students"""
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            
            # Read CSV file
            try:
                decoded_file = csv_file.read().decode('utf-8')
                csv_data = csv.DictReader(io.StringIO(decoded_file))
                
                success_count = 0
                error_count = 0
                errors = []
                
                for row in csv_data:
                    try:
                        # Parse date
                        date_str = row['date_of_birth'].strip()
                        try:
                            if '/' in date_str:
                                date_obj = datetime.strptime(date_str, '%d/%m/%Y').date()
                            else:
                                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                        except ValueError:
                            errors.append(f"Row {csv_data.line_num}: Invalid date format for {row.get('first_name', 'Unknown')}")
                            error_count += 1
                            continue
                        
                        # Get class
                        try:
                            class_obj = Class.objects.get(name=row['current_class'].strip())
                        except Class.DoesNotExist:
                            errors.append(f"Row {csv_data.line_num}: Class '{row['current_class']}' not found for {row.get('first_name', 'Unknown')}")
                            error_count += 1
                            continue
                        
                        # Generate username from email
                        email = row['email'].strip()
                        username = email.split('@')[0]
                        
                        # Check if user already exists
                        if User.objects.filter(username=username).exists():
                            username = f"{username}_{row['student_id']}"
                        
                        # Create user
                        user = User.objects.create_user(
                            username=username,
                            email=email,
                            password='changeme123',
                            first_name=row['first_name'].strip(),
                            last_name=row['last_name'].strip()
                        )
                        
                        # Create student
                        student = Student.objects.create(
                            user=user,
                            student_id=row['student_id'].strip(),
                            date_of_birth=date_obj,
                            gender=row['gender'].strip().upper(),
                            current_class=class_obj
                        )
                        
                        success_count += 1
                        
                    except Exception as e:
                        errors.append(f"Row {csv_data.line_num}: Error creating student {row.get('first_name', 'Unknown')} - {str(e)}")
                        error_count += 1
                
                if success_count > 0:
                    messages.success(request, f'Successfully created {success_count} students!')
                if error_count > 0:
                    messages.warning(request, f'Failed to create {error_count} students. Check the errors below.')
                    for error in errors[:10]:  # Show first 10 errors
                        messages.error(request, error)
                    if len(errors) > 10:
                        messages.error(request, f"... and {len(errors) - 10} more errors.")
                
                return redirect('academics:student_list')
                
            except Exception as e:
                messages.error(request, f'Error processing CSV file: {str(e)}')
    else:
        form = CSVUploadForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'academics/student_csv_upload.html', context)


@login_required
def teacher_csv_upload(request):
    """Handle CSV upload for teachers"""
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            
            # Read CSV file
            try:
                decoded_file = csv_file.read().decode('utf-8')
                csv_data = csv.DictReader(io.StringIO(decoded_file))
                
                success_count = 0
                error_count = 0
                errors = []
                
                for row in csv_data:
                    try:
                        # Generate username from email
                        email = row['email'].strip()
                        username = email.split('@')[0]
                        
                        # Check if user already exists
                        if User.objects.filter(username=username).exists():
                            username = f"{username}_{row['employee_id']}"
                        
                        # Create user
                        user = User.objects.create_user(
                            username=username,
                            email=email,
                            password='changeme123',
                            first_name=row['first_name'].strip(),
                            last_name=row['last_name'].strip()
                        )
                        
                        # Get subject if provided
                        subject = None
                        if row.get('subject'):
                            try:
                                subject = Subject.objects.get(name=row['subject'].strip())
                            except Subject.DoesNotExist:
                                pass  # Subject not found, but continue with teacher creation
                        
                        # Create teacher
                        teacher = Teacher.objects.create(
                            user=user,
                            employee_id=row['employee_id'].strip(),
                            phone=row.get('phone', '').strip(),
                            subject=subject
                        )
                        
                        success_count += 1
                        
                    except Exception as e:
                        errors.append(f"Row {csv_data.line_num}: Error creating teacher {row.get('first_name', 'Unknown')} - {str(e)}")
                        error_count += 1
                
                if success_count > 0:
                    messages.success(request, f'Successfully created {success_count} teachers!')
                if error_count > 0:
                    messages.warning(request, f'Failed to create {error_count} teachers. Check the errors below.')
                    for error in errors[:10]:  # Show first 10 errors
                        messages.error(request, error)
                    if len(errors) > 10:
                        messages.error(request, f"... and {len(errors) - 10} more errors.")
                
                return redirect('academics:teacher_list')
                
            except Exception as e:
                messages.error(request, f'Error processing CSV file: {str(e)}')
    else:
        form = CSVUploadForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'academics/teacher_csv_upload.html', context)


@login_required
def class_csv_upload(request):
    """Handle CSV upload for classes"""
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            
            # Read CSV file
            try:
                decoded_file = csv_file.read().decode('utf-8')
                csv_data = csv.DictReader(io.StringIO(decoded_file))
                
                success_count = 0
                error_count = 0
                errors = []
                
                for row in csv_data:
                    try:
                        # Create class
                        class_obj = Class.objects.create(
                            name=row['name'].strip(),
                            description=row.get('description', '').strip()
                        )
                        
                        success_count += 1
                        
                    except Exception as e:
                        errors.append(f"Row {csv_data.line_num}: Error creating class {row.get('name', 'Unknown')} - {str(e)}")
                        error_count += 1
                
                if success_count > 0:
                    messages.success(request, f'Successfully created {success_count} classes!')
                if error_count > 0:
                    messages.warning(request, f'Failed to create {error_count} classes. Check the errors below.')
                    for error in errors[:10]:  # Show first 10 errors
                        messages.error(request, error)
                    if len(errors) > 10:
                        messages.error(request, f"... and {len(errors) - 10} more errors.")
                
                return redirect('academics:class_list')
                
            except Exception as e:
                messages.error(request, f'Error processing CSV file: {str(e)}')
    else:
        form = CSVUploadForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'academics/class_csv_upload.html', context)


@login_required
def clean_all_students(request):
    """Delete all students and their associated users"""
    if request.method == 'POST':
        try:
            # Get all students
            students = Student.objects.all()
            student_count = students.count()
            
            # Get all associated users
            user_ids = list(students.values_list('user_id', flat=True))
            
            # Delete students first (this will cascade to related data)
            students.delete()
            
            # Delete associated users
            User.objects.filter(id__in=user_ids).delete()
            
            messages.success(request, f'Successfully deleted {student_count} students and their associated data!')
            return redirect('academics:student_list')
            
        except Exception as e:
            messages.error(request, f'Error deleting students: {str(e)}')
            return redirect('academics:student_list')
    
    # Show confirmation page
    student_count = Student.objects.count()
    context = {
        'item_type': 'students',
        'item_count': student_count,
        'back_url': 'academics:student_list',
    }
    
    return render(request, 'academics/clean_all_confirm.html', context)


@login_required
def clean_all_teachers(request):
    """Delete all teachers and their associated users"""
    if request.method == 'POST':
        try:
            # Get all teachers
            teachers = Teacher.objects.all()
            teacher_count = teachers.count()
            
            # Get all associated users
            user_ids = list(teachers.values_list('user_id', flat=True))
            
            # Delete teachers first (this will cascade to related data)
            teachers.delete()
            
            # Delete associated users
            User.objects.filter(id__in=user_ids).delete()
            
            messages.success(request, f'Successfully deleted {teacher_count} teachers and their associated data!')
            return redirect('academics:teacher_list')
            
        except Exception as e:
            messages.error(request, f'Error deleting teachers: {str(e)}')
            return redirect('academics:teacher_list')
    
    # Show confirmation page
    teacher_count = Teacher.objects.count()
    context = {
        'item_type': 'teachers',
        'item_count': teacher_count,
        'back_url': 'academics:teacher_list',
    }
    
    return render(request, 'academics/clean_all_confirm.html', context)


@login_required
def clean_all_subjects(request):
    """Delete all subjects"""
    if request.method == 'POST':
        try:
            # Get all subjects
            subjects = Subject.objects.all()
            subject_count = subjects.count()
            
            # Delete subjects
            subjects.delete()
            
            messages.success(request, f'Successfully deleted {subject_count} subjects!')
            return redirect('academics:subject_list')
            
        except Exception as e:
            messages.error(request, f'Error deleting subjects: {str(e)}')
            return redirect('academics:subject_list')
    
    # Show confirmation page
    subject_count = Subject.objects.count()
    context = {
        'item_type': 'subjects',
        'item_count': subject_count,
        'back_url': 'academics:subject_list',
    }
    
    return render(request, 'academics/clean_all_confirm.html', context)


@login_required
def clean_all_classes(request):
    """Delete all classes"""
    if request.method == 'POST':
        try:
            # Get all classes
            classes = Class.objects.all()
            class_count = classes.count()
            
            # Delete classes
            classes.delete()
            
            messages.success(request, f'Successfully deleted {class_count} classes!')
            return redirect('academics:class_list')
            
        except Exception as e:
            messages.error(request, f'Error deleting classes: {str(e)}')
            return redirect('academics:class_list')
    
    # Show confirmation page
    class_count = Class.objects.count()
    context = {
        'item_type': 'classes',
        'item_count': class_count,
        'back_url': 'academics:class_list',
    }
    
    return render(request, 'academics/clean_all_confirm.html', context)


@login_required
def clean_all_data(request):
    """Delete all data (students, teachers, subjects, classes, marks, attendance)"""
    if request.method == 'POST':
        try:
            # Get counts before deletion
            student_count = Student.objects.count()
            teacher_count = Teacher.objects.count()
            subject_count = Subject.objects.count()
            class_count = Class.objects.count()
            mark_count = Mark.objects.count()
            attendance_count = Attendance.objects.count()
            
            # Delete all data in the correct order to avoid foreign key constraints
            Mark.objects.all().delete()
            Attendance.objects.all().delete()
            ClassSubject.objects.all().delete()
            
            # Get user IDs before deleting students and teachers
            student_user_ids = list(Student.objects.values_list('user_id', flat=True))
            teacher_user_ids = list(Teacher.objects.values_list('user_id', flat=True))
            
            # Delete students and teachers
            Student.objects.all().delete()
            Teacher.objects.all().delete()
            
            # Delete associated users
            all_user_ids = student_user_ids + teacher_user_ids
            User.objects.filter(id__in=all_user_ids).delete()
            
            # Delete subjects and classes
            Subject.objects.all().delete()
            Class.objects.all().delete()
            
            messages.success(request, f'Successfully cleaned all data! Deleted: {student_count} students, {teacher_count} teachers, {subject_count} subjects, {class_count} classes, {mark_count} marks, {attendance_count} attendance records.')
            return redirect('academics:dashboard')
            
        except Exception as e:
            messages.error(request, f'Error cleaning all data: {str(e)}')
            return redirect('academics:dashboard')
    
    # Show confirmation page
    student_count = Student.objects.count()
    teacher_count = Teacher.objects.count()
    subject_count = Subject.objects.count()
    class_count = Class.objects.count()
    mark_count = Mark.objects.count()
    attendance_count = Attendance.objects.count()
    
    context = {
        'item_type': 'all data',
        'item_count': student_count + teacher_count + subject_count + class_count + mark_count + attendance_count,
        'back_url': 'academics:dashboard',
        'details': {
            'students': student_count,
            'teachers': teacher_count,
            'subjects': subject_count,
            'classes': class_count,
            'marks': mark_count,
            'attendance': attendance_count,
        }
    }
    
    return render(request, 'academics/clean_all_confirm.html', context)
