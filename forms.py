from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class UploadForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=200)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=1000)])
    subject_id = SelectField('Subject', validators=[DataRequired()], coerce=int)
    file = FileField('File', validators=[
        FileRequired(),
        FileAllowed(['pdf', 'doc', 'docx', 'ppt', 'pptx', 'txt', 'zip', 'rar'], 
                   'Only PDF, DOC, PPT, TXT, and ZIP files are allowed!')
    ])
    submit = SubmitField('Upload Resource')

class SubjectForm(FlaskForm):
    name = StringField('Subject Name', validators=[DataRequired(), Length(min=3, max=100)])
    code = StringField('Subject Code', validators=[Optional(), Length(max=20)])
    year_id = SelectField('Academic Year', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Add Subject')
