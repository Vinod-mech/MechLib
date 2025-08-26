# Overview

ANITS Digital Library is a Flask-based web application designed to serve as an academic resource portal for the Mechanical Engineering Department at ANITS (Anil Neerukonda Institute of Technology & Sciences). The system allows students and faculty to upload, organize, and access educational materials categorized by academic years and subjects. It features a hierarchical structure organizing resources by year → subject → individual files, with user authentication, file upload capabilities, and search functionality.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask for server-side rendering
- **UI Framework**: Bootstrap 5 with dark theme for responsive design
- **JavaScript**: Vanilla JavaScript for client-side interactions (file upload progress, tooltips, auto-hiding alerts)
- **Icons**: Font Awesome 6.4.0 for consistent iconography
- **CSS**: Custom CSS for hover effects and styling enhancements

## Backend Architecture
- **Web Framework**: Flask with modular structure separating routes, models, forms, and utilities
- **Database ORM**: SQLAlchemy with declarative base for database operations
- **Authentication**: Flask-Login for session management with admin role support
- **Form Handling**: WTForms with Flask-WTF for form validation and CSRF protection
- **File Handling**: Werkzeug utilities for secure file uploads with extension validation

## Data Model
- **Hierarchical Structure**: Year → Subject → Resource relationship using foreign keys
- **User Management**: User model with admin privileges and upload tracking
- **File Metadata**: Resources store original filename, file size, type, and download statistics
- **Cascade Deletions**: Configured to maintain referential integrity

## Security Features
- **Password Hashing**: Werkzeug security for password encryption
- **File Validation**: Restricted file types (PDF, DOC, PPT, TXT, ZIP, RAR) with size limits (50MB)
- **CSRF Protection**: Built-in Flask-WTF CSRF tokens
- **Secure Filenames**: Werkzeug secure_filename for upload safety
- **Session Management**: Configurable session secrets and remember-me functionality

## File Storage
- **Local Storage**: Files stored in 'uploads' directory with UUID-based naming
- **Metadata Tracking**: Original filenames preserved while using secure internal names
- **Size Limits**: 50MB maximum file size with client-side validation

# External Dependencies

## Core Framework Dependencies
- **Flask**: Web application framework
- **Flask-SQLAlchemy**: Database ORM integration
- **Flask-Login**: User session management
- **Flask-WTF**: Form handling and validation
- **WTForms**: Form field definitions and validators

## Frontend Dependencies
- **Bootstrap 5**: CSS framework via CDN (dark theme variant)
- **Font Awesome 6.4.0**: Icon library via CDN
- **Bootstrap JavaScript**: Client-side components and interactions

## Database
- **SQLite**: Default database for development (configurable via DATABASE_URL environment variable)
- **Connection Pooling**: Configured with pool recycling and pre-ping for reliability

## Development Tools
- **Werkzeug**: WSGI utilities and development server
- **ProxyFix**: Middleware for handling reverse proxy headers

## Environment Configuration
- **SESSION_SECRET**: Environment variable for session encryption
- **DATABASE_URL**: Configurable database connection string
- **File Upload Directory**: Configurable upload path with automatic creation