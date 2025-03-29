from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, TextAreaField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class AppointmentForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=20)])
    department = SelectField('Department', 
                           choices=[
                               ('', 'Select Department'),
                               ('cardiology', 'Cardiology'),
                               ('neurology', 'Neurology'),
                               ('orthopedics', 'Orthopedics'),
                               ('pediatrics', 'Pediatrics'),
                               ('gynecology', 'Gynecology'),
                               ('ophthalmology', 'Ophthalmology'),
                               ('dermatology', 'Dermatology'),
                               ('urology', 'Urology'),
                               ('ent', 'ENT'),
                               ('general', 'General Medicine')
                           ], 
                           validators=[DataRequired()])
    doctor = SelectField('Doctor', 
                       choices=[
                           ('', 'Select Doctor'),
                           ('dr_sharma', 'Dr. Sharma'),
                           ('dr_patel', 'Dr. Patel'),
                           ('dr_singh', 'Dr. Singh'),
                           ('dr_gupta', 'Dr. Gupta'),
                           ('dr_verma', 'Dr. Verma')
                       ], 
                       validators=[DataRequired()])
    date = DateField('Preferred Date', format='%Y-%m-%d', validators=[DataRequired()])
    time = SelectField('Preferred Time', 
                     choices=[
                         ('', 'Select Time'),
                         ('morning', 'Morning (9:00 AM - 12:00 PM)'),
                         ('afternoon', 'Afternoon (1:00 PM - 4:00 PM)'),
                         ('evening', 'Evening (5:00 PM - 8:00 PM)')
                     ], 
                     validators=[DataRequired()])
    message = TextAreaField('Message (Optional)', validators=[Length(max=500)])
    submit = SubmitField('Book Appointment')

class ContactForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=2, max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Send Message')

class NewsletterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Subscribe')
