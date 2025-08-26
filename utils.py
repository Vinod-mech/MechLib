import os
from app import db
from models import Year, Subject

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'ppt', 'pptx', 'txt', 'zip', 'rar'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_size(file_path):
    """Get file size in bytes"""
    return os.path.getsize(file_path)

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f} {size_names[i]}"

def populate_initial_data():
    """Populate initial years and subjects based on ANITS ME syllabus"""
    
    # Clear existing data to ensure clean structure
    from models import Year, Subject, Resource
    Resource.query.delete()
    Subject.query.delete() 
    Year.query.delete()
    db.session.commit()
    
    # Define years
    years_data = [
        {'name': '1st Year', 'order': 1},
        {'name': '2nd Year', 'order': 2},
        {'name': '3rd Year', 'order': 3},
        {'name': '4th Year', 'order': 4},
        {'name': 'Electives', 'order': 5}
    ]
    
    # Define subjects by year
    subjects_data = {
        1: [  # 1st Year
            'Engineering Mathematics',
            'Engineering Physics',
            'Engineering Chemistry',
            'Biology for Engineers',
            'Engineering Drawing',
            'CAD',
            'English',
            'C Language',
            'Basic Electrical Engineering',
            'Basic Electronic Engineering',
            'Quantitative Aptitude',
            'Verbal Aptitude'
        ],
        2: [  # 2nd Year
            'Material Science and Metallurgy',
            'Engineering Mechanics',
            'Strength of Materials',
            'Basic Thermodynamics',
            'Manufacturing Technology',
            'Applied Thermal Engineering-1',
            'Kinematics of Machinery',
            'Metal Cutting, Machine Tools and Metrology',
            'Computer-Aided Modelling'
        ],
        3: [  # 3rd Year
            'Design Thinking',
            'Dynamics of Machinery',
            'Applied Thermal Engineering-2',
            'Design of Machine Elements-1',
            'Finite Element Analysis',
            'Fluid Mechanics & Hydraulic Machinery',
            'Design of Machine Elements-2',
            'Python',
            'Data Structures using Python',
            'Database Management System'
        ],
        4: [  # 4th Year
            'Heat Transfer',
            'Automotive Engineering'
        ],
        5: [  # Electives
            'Production Planning & Control',
            'Gas Turbine & Jet Propulsions',
            'Automation in Manufacturing',
            'Non-Destructive Testing',
            'Refrigeration and Air-conditioning',
            'Power Plant Engineering',
            'Nano Technology',
            'Quality & Reliability Engineering',
            'Mechanical Measurements',
            'Computational Fluid Dynamics',
            'Condition Monitoring',
            'Industrial Tribology',
            'Non-conventional Energy Sources',
            'Managerial Economics & Financial Accountancy',
            'Unconventional Machining Process',
            'Artificial Intelligence',
            'Operational Research',
            'Alternative Fuels',
            'Advanced Mechanics of Materials',
            'Product Design & Manufacturing',
            'Industrial Engineering Management',
            'Statistical Quality Control',
            'Entrepreneurship Development',
            'Supply Chain Management'
        ]
    }
    
    # Create years
    year_objects = {}
    for year_data in years_data:
        year = Year(**year_data)
        db.session.add(year)
        db.session.flush()  # Get the ID
        year_objects[year_data['order']] = year
    
    # Create subjects
    for year_order, subject_names in subjects_data.items():
        year = year_objects[year_order]
        for subject_name in subject_names:
            subject = Subject(name=subject_name, year_id=year.id)
            db.session.add(subject)
    
    db.session.commit()
