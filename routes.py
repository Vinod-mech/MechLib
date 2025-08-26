import os
import uuid
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, send_file, jsonify, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy import or_
from app import app, db
from models import User, Year, Subject, Resource
from forms import LoginForm, UploadForm, SubjectForm
from utils import allowed_file, get_file_size, populate_initial_data

# Data initialization is handled in app.py after db.create_all()

@app.route('/')
def index():
    """Home page showing all years with statistics"""
    years = Year.query.order_by(Year.order).all()
    total_resources = Resource.query.count()
    
    year_stats = []
    for year in years:
        subject_count = Subject.query.filter_by(year_id=year.id).count()
        resource_count = db.session.query(Resource).join(Subject).filter(Subject.year_id == year.id).count()
        year_stats.append({
            'year': year,
            'subject_count': subject_count,
            'resource_count': resource_count
        })
    
    return render_template('index.html', year_stats=year_stats, total_resources=total_resources)

@app.route('/year/<int:year_id>')
def year_view(year_id):
    """View all subjects for a specific year"""
    year = Year.query.get_or_404(year_id)
    subjects = Subject.query.filter_by(year_id=year_id).all()
    
    subject_stats = []
    for subject in subjects:
        resource_count = Resource.query.filter_by(subject_id=subject.id).count()
        subject_stats.append({
            'subject': subject,
            'resource_count': resource_count
        })
    
    return render_template('year.html', year=year, subject_stats=subject_stats)

@app.route('/subject/<int:subject_id>')
def subject_view(subject_id):
    """View all resources for a specific subject"""
    subject = Subject.query.get_or_404(subject_id)
    resources = Resource.query.filter_by(subject_id=subject_id).order_by(Resource.upload_date.desc()).all()
    
    return render_template('subject.html', subject=subject, resources=resources)

@app.route('/search')
def search():
    """Search for resources"""
    query = request.args.get('q', '').strip()
    year_filter = request.args.get('year', '')
    subject_filter = request.args.get('subject', '')
    
    resources = []
    subjects = Subject.query.all()
    years = Year.query.order_by(Year.order).all()
    
    if query or year_filter or subject_filter:
        resource_query = Resource.query.join(Subject).join(Year)
        
        if query:
            resource_query = resource_query.filter(
                or_(
                    Resource.title.ilike(f'%{query}%'),
                    Resource.description.ilike(f'%{query}%'),
                    Subject.name.ilike(f'%{query}%')
                )
            )
        
        if year_filter:
            resource_query = resource_query.filter(Year.id == year_filter)
        
        if subject_filter:
            resource_query = resource_query.filter(Subject.id == subject_filter)
        
        resources = resource_query.order_by(Resource.upload_date.desc()).all()
    
    return render_template('search.html', 
                         resources=resources, 
                         query=query, 
                         subjects=subjects, 
                         years=years,
                         year_filter=year_filter,
                         subject_filter=subject_filter)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_resource():
    """Upload a new resource"""
    form = UploadForm()
    form.subject_id.choices = [(s.id, f"{s.year.name} - {s.name}") 
                              for s in Subject.query.join(Year).order_by(Year.order, Subject.name).all()]
    
    if form.validate_on_submit():
        file = form.file.data
        if file and allowed_file(file.filename):
            # Generate secure filename
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            
            try:
                file.save(file_path)
                file_size = get_file_size(file_path)
                
                # Create resource record
                resource = Resource(
                    title=form.title.data,
                    description=form.description.data,
                    filename=unique_filename,
                    original_filename=filename,
                    file_size=file_size,
                    file_type=filename.rsplit('.', 1)[1].lower() if '.' in filename else '',
                    subject_id=form.subject_id.data,
                    uploaded_by=current_user.id
                )
                
                db.session.add(resource)
                db.session.commit()
                
                flash('Resource uploaded successfully!', 'success')
                return redirect(url_for('subject_view', subject_id=form.subject_id.data))
                
            except Exception as e:
                if os.path.exists(file_path):
                    os.remove(file_path)
                flash(f'Error uploading file: {str(e)}', 'danger')
        else:
            flash('Invalid file type. Please upload PDF, DOC, DOCX, PPT, PPTX, TXT, or ZIP files.', 'danger')
    
    return render_template('upload.html', form=form)

@app.route('/download/<int:resource_id>')
def download_resource(resource_id):
    """Download a resource file"""
    resource = Resource.query.get_or_404(resource_id)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], resource.filename)
    
    if not os.path.exists(file_path):
        flash('File not found.', 'danger')
        return redirect(url_for('subject_view', subject_id=resource.subject_id))
    
    # Increment download count
    resource.download_count += 1
    db.session.commit()
    
    return send_file(file_path, as_attachment=True, download_name=resource.original_filename)

@app.route('/view/<int:resource_id>')
def view_resource(resource_id):
    """View a PDF file inline in the browser"""
    resource = Resource.query.get_or_404(resource_id)
    
    # Only allow viewing of PDF files
    if resource.get_file_extension().lower() != 'pdf':
        flash('Only PDF files can be viewed inline.', 'warning')
        return redirect(url_for('subject_view', subject_id=resource.subject_id))
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], resource.filename)
    
    if not os.path.exists(file_path):
        flash('File not found.', 'danger')
        return redirect(url_for('subject_view', subject_id=resource.subject_id))
    
    # Serve PDF file to be viewed inline in browser
    return send_file(file_path, as_attachment=False, mimetype='application/pdf')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_panel():
    """Admin panel for managing resources and subjects"""
    if not current_user.is_admin:
        abort(403)
    
    years = Year.query.order_by(Year.order).all()
    subjects = Subject.query.join(Year).order_by(Year.order, Subject.name).all()
    resources = Resource.query.join(Subject).join(Year).order_by(Resource.upload_date.desc()).limit(20).all()
    
    stats = {
        'total_users': User.query.count(),
        'total_resources': Resource.query.count(),
        'total_subjects': Subject.query.count(),
        'total_downloads': db.session.query(db.func.sum(Resource.download_count)).scalar() or 0
    }
    
    return render_template('admin.html', 
                         years=years, 
                         subjects=subjects, 
                         resources=resources, 
                         stats=stats)

@app.route('/admin/add_subject', methods=['POST'])
@login_required
def add_subject():
    """Add a new subject (admin only)"""
    if not current_user.is_admin:
        abort(403)
    
    form = SubjectForm()
    form.year_id.choices = [(y.id, y.name) for y in Year.query.order_by(Year.order).all()]
    
    if form.validate_on_submit():
        subject = Subject(
            name=form.name.data,
            code=form.code.data,
            year_id=form.year_id.data
        )
        db.session.add(subject)
        db.session.commit()
        flash('Subject added successfully!', 'success')
    else:
        flash('Error adding subject. Please check your input.', 'danger')
    
    return redirect(url_for('admin_panel'))

@app.route('/admin/delete_resource/<int:resource_id>', methods=['POST'])
@login_required
def delete_resource(resource_id):
    """Delete a resource (admin only)"""
    if not current_user.is_admin:
        abort(403)
    
    resource = Resource.query.get_or_404(resource_id)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], resource.filename)
    
    try:
        # Delete file from filesystem
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Delete from database
        db.session.delete(resource)
        db.session.commit()
        
        flash('Resource deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting resource: {str(e)}', 'danger')
    
    return redirect(url_for('admin_panel'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
