from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from academics.models import Class, Subject, Teacher, Student, ClassSubject, Mark, Attendance
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the database with sample data for demonstration'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create Classes
        classes = []
        class_names = ['Grade 9A', 'Grade 9B', 'Grade 10A', 'Grade 10B', 'Grade 11A', 'Grade 11B']
        for name in class_names:
            class_obj, created = Class.objects.get_or_create(
                name=name,
                defaults={'description': f'Class {name}'}
            )
            classes.append(class_obj)
            if created:
                self.stdout.write(f'Created class: {name}')
        
        # Create Subjects
        subjects = []
        subject_data = [
            ('MATH', 'Mathematics', 4),
            ('ENG', 'English Literature', 3),
            ('SCI', 'Science', 4),
            ('HIST', 'History', 3),
            ('GEO', 'Geography', 3),
            ('PHY', 'Physics', 4),
            ('CHEM', 'Chemistry', 4),
            ('BIO', 'Biology', 4),
            ('COMP', 'Computer Science', 3),
            ('ART', 'Art & Design', 2),
        ]
        
        for code, name, credits in subject_data:
            subject, created = Subject.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'credits': credits,
                    'description': f'Subject: {name}'
                }
            )
            subjects.append(subject)
            if created:
                self.stdout.write(f'Created subject: {name}')
        
        # Create Teachers
        teachers = []
        teacher_data = [
            ('John', 'Smith', 'T001', 'john.smith@school.com', '555-0101'),
            ('Sarah', 'Johnson', 'T002', 'sarah.johnson@school.com', '555-0102'),
            ('Michael', 'Brown', 'T003', 'michael.brown@school.com', '555-0103'),
            ('Emily', 'Davis', 'T004', 'emily.davis@school.com', '555-0104'),
            ('David', 'Wilson', 'T005', 'david.wilson@school.com', '555-0105'),
            ('Lisa', 'Anderson', 'T006', 'lisa.anderson@school.com', '555-0106'),
        ]
        
        for first_name, last_name, emp_id, email, phone in teacher_data:
            user, created = User.objects.get_or_create(
                username=f'{first_name.lower()}.{last_name.lower()}',
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'is_staff': True,
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            
            teacher, created = Teacher.objects.get_or_create(
                employee_id=emp_id,
                defaults={
                    'user': user,
                    'phone': phone,
                    'address': f'Address for {first_name} {last_name}',
                    'date_of_birth': date(1980, 1, 1) + timedelta(days=random.randint(0, 10000)),
                    'hire_date': date(2020, 1, 1) + timedelta(days=random.randint(0, 1000)),
                }
            )
            teachers.append(teacher)
            if created:
                self.stdout.write(f'Created teacher: {first_name} {last_name}')
        
        # Assign subjects to teachers
        subject_assignments = [
            (0, [0, 5]),  # John Smith - Math, Physics
            (1, [1, 6]),  # Sarah Johnson - English, Chemistry
            (2, [2, 7]),  # Michael Brown - Science, Biology
            (3, [3, 8]),  # Emily Davis - History, Computer Science
            (4, [4, 9]),  # David Wilson - Geography, Art
            (5, [0, 2]),  # Lisa Anderson - Math, Science
        ]
        
        for teacher_idx, subject_indices in subject_assignments:
            teacher = teachers[teacher_idx]
            for subject_idx in subject_indices:
                teacher.subjects.add(subjects[subject_idx])
        
        # Create Students
        students = []
        student_data = [
            ('Alice', 'Johnson', 'S001', 'F', 'alice.johnson@student.com'),
            ('Bob', 'Williams', 'S002', 'M', 'bob.williams@student.com'),
            ('Carol', 'Brown', 'S003', 'F', 'carol.brown@student.com'),
            ('David', 'Jones', 'S004', 'M', 'david.jones@student.com'),
            ('Eva', 'Garcia', 'S005', 'F', 'eva.garcia@student.com'),
            ('Frank', 'Miller', 'S006', 'M', 'frank.miller@student.com'),
            ('Grace', 'Davis', 'S007', 'F', 'grace.davis@student.com'),
            ('Henry', 'Rodriguez', 'S008', 'M', 'henry.rodriguez@student.com'),
            ('Ivy', 'Martinez', 'S009', 'F', 'ivy.martinez@student.com'),
            ('Jack', 'Anderson', 'S010', 'M', 'jack.anderson@student.com'),
        ]
        
        for first_name, last_name, student_id, gender, email in student_data:
            user, created = User.objects.get_or_create(
                username=f'{first_name.lower()}.{last_name.lower()}',
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            
            student, created = Student.objects.get_or_create(
                student_id=student_id,
                defaults={
                    'user': user,
                    'gender': gender,
                    'phone': f'555-{random.randint(1000, 9999)}',
                    'address': f'Address for {first_name} {last_name}',
                    'parent_name': f'Parent of {first_name} {last_name}',
                    'parent_phone': f'555-{random.randint(1000, 9999)}',
                    'parent_email': f'parent.{first_name.lower()}@email.com',
                    'date_of_birth': date(2005, 1, 1) + timedelta(days=random.randint(0, 2000)),
                    'current_class': random.choice(classes),
                    'enrollment_date': date(2023, 9, 1) + timedelta(days=random.randint(0, 100)),
                }
            )
            students.append(student)
            if created:
                self.stdout.write(f'Created student: {first_name} {last_name}')
        
        # Create Class-Subject assignments
        class_subjects = []
        academic_year = "2024-2025"
        semester = "First Semester"
        
        for class_obj in classes:
            # Assign 5-6 subjects to each class
            class_subject_list = random.sample(subjects, min(6, len(subjects)))
            for subject in class_subject_list:
                teacher = random.choice(teachers)
                class_subject, created = ClassSubject.objects.get_or_create(
                    class_obj=class_obj,
                    subject=subject,
                    academic_year=academic_year,
                    semester=semester,
                    defaults={'teacher': teacher}
                )
                class_subjects.append(class_subject)
                if created:
                    self.stdout.write(f'Created class-subject: {class_obj.name} - {subject.name}')
        
        # Create Marks
        mark_types = ['assignment', 'quiz', 'midterm', 'final', 'project']
        
        for student in students:
            # Get class subjects for student's class
            student_class_subjects = [cs for cs in class_subjects if cs.class_obj == student.current_class]
            
            for class_subject in student_class_subjects:
                # Create 2-4 marks per subject
                num_marks = random.randint(2, 4)
                for i in range(num_marks):
                    mark_type = random.choice(mark_types)
                    score = random.randint(60, 100)
                    max_score = 100
                    
                    # Ensure unique mark
                    mark_date = date(2024, 9, 1) + timedelta(days=random.randint(0, 100))
                    
                    mark, created = Mark.objects.get_or_create(
                        student=student,
                        class_subject=class_subject,
                        mark_type=mark_type,
                        date_given=mark_date,
                        defaults={
                            'score': score,
                            'max_score': max_score,
                            'remarks': f'Good work on {mark_type}'
                        }
                    )
                    if created:
                        self.stdout.write(f'Created mark: {student.full_name} - {class_subject.subject.name} - {mark_type}')
        
        # Create Attendance records
        start_date = date(2024, 9, 1)
        end_date = date(2024, 12, 31)
        current_date = start_date
        
        while current_date <= end_date:
            # Skip weekends
            if current_date.weekday() < 5:  # Monday to Friday
                for student in students:
                    for class_subject in class_subjects:
                        if class_subject.class_obj == student.current_class:
                            # 95% attendance rate
                            is_present = random.random() < 0.95
                            
                            attendance, created = Attendance.objects.get_or_create(
                                student=student,
                                class_subject=class_subject,
                                date=current_date,
                                defaults={
                                    'is_present': is_present,
                                    'remarks': 'Regular attendance' if is_present else 'Absent'
                                }
                            )
                            if created:
                                self.stdout.write(f'Created attendance: {student.full_name} - {current_date} - {"Present" if is_present else "Absent"}')
            
            current_date += timedelta(days=1)
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        )
        self.stdout.write(f'Created {len(classes)} classes')
        self.stdout.write(f'Created {len(subjects)} subjects')
        self.stdout.write(f'Created {len(teachers)} teachers')
        self.stdout.write(f'Created {len(students)} students')
        self.stdout.write(f'Created {len(class_subjects)} class-subject assignments')
        self.stdout.write(f'Created {Mark.objects.count()} marks')
        self.stdout.write(f'Created {Attendance.objects.count()} attendance records') 