import os
import logging
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_wtf.csrf import CSRFProtect

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# configure the database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///arvindu_hospital.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize CSRF protection
csrf = CSRFProtect(app)

# initialize the app with the extension, flask-sqlalchemy >= 3.0.x
db.init_app(app)

with app.app_context():
    # Make sure to import the models here or their tables won't be created
    import models  # noqa: F401
    db.create_all()

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/departments')
def departments():
    return render_template('departments.html')

@app.route('/doctors')
def doctors():
    return render_template('doctors.html')

@app.route('/patient-care')
def patient_care():
    return render_template('patient_care.html')

@app.route('/testimonials')
def testimonials():
    return render_template('testimonials.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/careers')
def careers():
    return render_template('careers.html')

@app.route('/news')
def news():
    return render_template('news.html')

@app.route('/csr')
def csr():
    return render_template('csr.html')

@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    from forms import AppointmentForm
    form = AppointmentForm()
    
    if form.validate_on_submit():
        # This would typically save to the database
        # For now, just flash a success message
        flash('Your appointment request has been submitted. We will contact you shortly.', 'success')
        return redirect(url_for('appointment'))
        
    return render_template('appointment.html', form=form)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    from forms import ContactForm
    form = ContactForm()
    
    if form.validate_on_submit():
        # This would typically save to the database or send an email
        # For now, just flash a success message
        flash('Your message has been sent. We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
        
    return render_template('contact.html', form=form)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('base.html', error_message="404 - Page Not Found"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('base.html', error_message="500 - Internal Server Error"), 500
