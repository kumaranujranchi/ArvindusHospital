from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, EmailField, TelField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class AppointmentForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = TelField('Phone Number', validators=[DataRequired(), Length(min=10, max=20)])
    department = SelectField('Department', choices=[
        ('', 'Select Department'),
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('orthopedics', 'Orthopedics'),
        ('pediatrics', 'Pediatrics'),
        ('ophthalmology', 'Ophthalmology'),
        ('dermatology', 'Dermatology'),
        ('gynecology', 'Gynecology'),
        ('urology', 'Urology'),
        ('ent', 'ENT'),
        ('dental', 'Dental')
    ], validators=[DataRequired()])
    doctor = SelectField('Doctor', choices=[
        ('', 'Select Doctor'),
        ('any', 'Any Doctor'),
        ('dr-sharma', 'Dr. Sharma'),
        ('dr-patel', 'Dr. Patel'),
        ('dr-gupta', 'Dr. Gupta'),
        ('dr-singh', 'Dr. Singh'),
        ('dr-kumar', 'Dr. Kumar')
    ], validators=[DataRequired()])
    date = DateField('Preferred Date', format='%Y-%m-%d', validators=[DataRequired()])
    time = SelectField('Preferred Time', choices=[
        ('', 'Select Time'),
        ('morning', 'Morning (9:00 AM - 12:00 PM)'),
        ('afternoon', 'Afternoon (12:00 PM - 3:00 PM)'),
        ('evening', 'Evening (3:00 PM - 6:00 PM)')
    ], validators=[DataRequired()])
    message = TextAreaField('Additional Information', validators=[Length(max=500)])
    submit = SubmitField('Book Appointment')

class ContactForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = TelField('Phone Number', validators=[DataRequired(), Length(min=10, max=20)])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=5, max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Send Message')
