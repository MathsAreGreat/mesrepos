from django.urls import path
from . import views

app_name = 'academics'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Students
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_create, name='student_create'),
    path('students/upload/', views.student_csv_upload, name='student_csv_upload'),
    path('students/clean-all/', views.clean_all_students, name='clean_all_students'),
    path('students/<str:student_id>/', views.student_detail, name='student_detail'),
    path('students/<str:student_id>/update/', views.student_update, name='student_update'),
    
    # Teachers
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/add/', views.teacher_create, name='teacher_create'),
    path('teachers/upload/', views.teacher_csv_upload, name='teacher_csv_upload'),
    path('teachers/clean-all/', views.clean_all_teachers, name='clean_all_teachers'),
    path('teachers/<str:employee_id>/', views.teacher_detail, name='teacher_detail'),
    path('teachers/<str:employee_id>/update/', views.teacher_update, name='teacher_update'),
    
    # Subjects
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/add/', views.subject_create, name='subject_create'),
    path('subjects/clean-all/', views.clean_all_subjects, name='clean_all_subjects'),
    path('subjects/<str:subject_code>/edit/', views.subject_update, name='subject_update'),
    path('subjects/<str:subject_code>/delete/', views.subject_delete, name='subject_delete'),
    
    # Classes
    path('classes/', views.class_list, name='class_list'),
    path('classes/add/', views.class_create, name='class_create'),
    path('classes/upload/', views.class_csv_upload, name='class_csv_upload'),
    path('classes/clean-all/', views.clean_all_classes, name='clean_all_classes'),
    path('classes/<int:class_id>/edit/', views.class_update, name='class_update'),
    path('classes/<int:class_id>/delete/', views.class_delete, name='class_delete'),
    
    # Management
    path('marks/', views.mark_management, name='mark_management'),
    path('attendance/', views.attendance_management, name='attendance_management'),
    
    # Reports
    path('reports/', views.reports, name='reports'),
    
    # Clean All Data
    path('clean-all-data/', views.clean_all_data, name='clean_all_data'),
] 