from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SelectField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class AppointmentForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=6, max=20)])
    department = SelectField('Department', 
                           choices=[
                               ('', 'Select Department'),
                               ('cardiology', 'Cardiology'),
                               ('neurology', 'Neurology'),
                               ('orthopedics', 'Orthopedics'),
                               ('pediatrics', 'Pediatrics'),
                               ('gynecology', 'Gynecology'),
                               ('dermatology', 'Dermatology'),
                               ('ophthalmology', 'Ophthalmology'),
                               ('ent', 'ENT'),
                               ('gastroenterology', 'Gastroenterology'),
                               ('oncology', 'Oncology')
                           ],
                           validators=[DataRequired()])
    doctor = SelectField('Doctor (Optional)', 
                        choices=[
                            ('', 'Select Doctor (Optional)'),
                            ('dr_sharma', 'Dr. Sharma'),
                            ('dr_patel', 'Dr. Patel'),
                            ('dr_singh', 'Dr. Singh'),
                            ('dr_gupta', 'Dr. Gupta'),
                            ('dr_kumar', 'Dr. Kumar')
                        ])
    date = DateField('Preferred Date', format='%Y-%m-%d', validators=[DataRequired()])
    time = SelectField('Preferred Time',
                      choices=[
                          ('', 'Select Time'),
                          ('morning', 'Morning (9AM - 12PM)'),
                          ('afternoon', 'Afternoon (12PM - 3PM)'),
                          ('evening', 'Evening (3PM - 6PM)')
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
