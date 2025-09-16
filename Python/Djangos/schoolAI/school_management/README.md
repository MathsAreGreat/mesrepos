# SchoolAI - School Management System

A comprehensive Django-based school management system for managing students, teachers, subjects, marks, and attendance.

## Features

- **Student Management**: Add, edit, and manage student information
- **Teacher Management**: Manage teacher profiles and assignments
- **Subject Management**: Organize subjects with credits and descriptions
- **Class Management**: Manage different grade levels and classes
- **Mark Management**: Record and track student marks for various assessment types
- **Attendance Tracking**: Monitor student attendance with detailed records
- **Reports**: Generate performance and attendance reports
- **Admin Interface**: Full-featured Django admin interface
- **Modern UI**: Responsive design with Bootstrap and Font Awesome

## Technology Stack

- **Backend**: Django 5.2.4
- **Database**: SQLite (can be easily changed to PostgreSQL/MySQL)
- **Frontend**: Bootstrap 5.3, Font Awesome 6.4
- **Package Manager**: UV (Python package manager)

## Quick Start

### Prerequisites

- Python 3.11+
- UV package manager

### Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd school_management
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Run migrations**:
   ```bash
   uv run python manage.py migrate
   ```

4. **Create a superuser** (optional - already created):
   ```bash
   uv run python manage.py createsuperuser
   ```

5. **Populate with sample data** (optional - already done):
   ```bash
   uv run python manage.py populate_sample_data
   ```

6. **Start the development server**:
   ```bash
   uv run python manage.py runserver
   ```

7. **Access the application**:
   - Main application: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/

## Default Credentials

### Admin User
- **Username**: admin
- **Password**: admin123

### Sample Users
The system comes with sample data including:

**Teachers:**
- john.smith / password123
- sarah.johnson / password123
- michael.brown / password123
- emily.davis / password123
- david.wilson / password123
- lisa.anderson / password123

**Students:**
- alice.johnson / password123
- bob.williams / password123
- carol.brown / password123
- david.jones / password123
- eva.garcia / password123
- frank.miller / password123
- grace.davis / password123
- henry.rodriguez / password123
- ivy.martinez / password123
- jack.anderson / password123

## Project Structure

```
school_management/
├── academics/                 # Main application
│   ├── models.py             # Database models
│   ├── views.py              # View functions
│   ├── admin.py              # Admin interface configuration
│   ├── urls.py               # URL patterns
│   ├── management/           # Management commands
│   │   └── commands/
│   │       └── populate_sample_data.py
│   └── templates/            # Application templates
│       └── academics/
│           └── dashboard.html
├── school_system/            # Django project settings
│   ├── settings.py           # Project configuration
│   └── urls.py               # Main URL configuration
├── templates/                # Global templates
│   ├── base.html             # Base template
│   └── registration/
│       └── login.html        # Login page
├── manage.py                 # Django management script
├── pyproject.toml            # Project dependencies
└── README.md                 # This file
```

## Models Overview

### Core Models

1. **Class**: Represents school classes/grade levels
2. **Subject**: Academic subjects with codes and credits
3. **Teacher**: Teacher profiles linked to Django User model
4. **Student**: Student profiles with personal and academic information
5. **ClassSubject**: Links classes, subjects, and teachers
6. **Mark**: Student marks for various assessment types
7. **Attendance**: Daily attendance records

### Key Features

- **Automatic Grade Calculation**: Marks are automatically converted to letter grades
- **Age Calculation**: Student ages are calculated automatically
- **Attendance Tracking**: Comprehensive attendance monitoring
- **Performance Analytics**: Built-in reporting and statistics

## Usage

### Dashboard
The main dashboard provides:
- Overview statistics (students, teachers, subjects, classes)
- Recent marks and attendance records
- Quick action buttons

### Student Management
- View all students with search and filter options
- Detailed student profiles with marks and attendance
- Student performance analytics

### Teacher Management
- Manage teacher profiles and assignments
- View teaching assignments and student lists

### Mark Management
- Add marks for different assessment types
- Track student performance over time
- Automatic grade calculation

### Attendance Management
- Mark daily attendance
- Track attendance patterns
- Generate attendance reports

### Reports
- Class performance reports
- Subject performance analysis
- Attendance statistics

## Customization

### Adding New Assessment Types
Edit the `MARK_TYPES` choices in `academics/models.py`:

```python
MARK_TYPES = [
    ('assignment', 'Assignment'),
    ('quiz', 'Quiz'),
    ('midterm', 'Midterm'),
    ('final', 'Final'),
    ('project', 'Project'),
    ('participation', 'Participation'),
    ('homework', 'Homework'),  # Add new types here
]
```

### Changing Database
To use PostgreSQL or MySQL, update the database settings in `school_system/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'schoolai_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Styling
The application uses Bootstrap 5.3 with custom CSS. Modify the styles in `templates/base.html` to customize the appearance.

## Development

### Running Tests
```bash
uv run python manage.py test
```

### Creating New Management Commands
```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
```

### Adding New Features
1. Create new models in `academics/models.py`
2. Add views in `academics/views.py`
3. Update URLs in `academics/urls.py`
4. Create templates in `academics/templates/academics/`
5. Register models in `academics/admin.py`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For support or questions, please open an issue in the repository or contact the development team.
