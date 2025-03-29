import os
import logging
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")

# configure the database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///hospital.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
# initialize the app with the extension, flask-sqlalchemy >= 3.0.x
db.init_app(app)

from forms import AppointmentForm, ContactForm, NewsletterForm

@app.route('/')
def index():
    newsletter_form = NewsletterForm()
    return render_template('index.html', newsletter_form=newsletter_form)

@app.route('/about')
def about():
    newsletter_form = NewsletterForm()
    return render_template('about.html', newsletter_form=newsletter_form)

@app.route('/departments')
def departments():
    newsletter_form = NewsletterForm()
    return render_template('departments.html', newsletter_form=newsletter_form)

@app.route('/find-doctor')
def find_doctor():
    newsletter_form = NewsletterForm()
    return render_template('find_doctor.html', newsletter_form=newsletter_form)

@app.route('/patient-care')
def patient_care():
    newsletter_form = NewsletterForm()
    return render_template('patient_care.html', newsletter_form=newsletter_form)

@app.route('/testimonials')
def testimonials():
    newsletter_form = NewsletterForm()
    return render_template('testimonials.html', newsletter_form=newsletter_form)

@app.route('/blog')
def blog():
    newsletter_form = NewsletterForm()
    return render_template('blog.html', newsletter_form=newsletter_form)

@app.route('/careers')
def careers():
    newsletter_form = NewsletterForm()
    return render_template('careers.html', newsletter_form=newsletter_form)

@app.route('/media')
def media():
    newsletter_form = NewsletterForm()
    return render_template('media.html', newsletter_form=newsletter_form)

@app.route('/csr')
def csr():
    newsletter_form = NewsletterForm()
    return render_template('csr.html', newsletter_form=newsletter_form)

@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    form = AppointmentForm()
    newsletter_form = NewsletterForm()
    
    if form.validate_on_submit():
        # In a real application, you would save this to a database
        flash('Your appointment request has been submitted! We will contact you shortly.', 'success')
        return redirect(url_for('appointment'))
        
    return render_template('appointment.html', form=form, newsletter_form=newsletter_form)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    newsletter_form = NewsletterForm()
    
    if form.validate_on_submit():
        # In a real application, you would save this to a database or send an email
        flash('Your message has been sent! We will get back to you as soon as possible.', 'success')
        return redirect(url_for('contact'))
        
    return render_template('contact.html', form=form, newsletter_form=newsletter_form)

@app.route('/subscribe', methods=['POST'])
def subscribe():
    form = NewsletterForm()
    if form.validate_on_submit():
        # In a real application, you would save this to a database
        flash('Thank you for subscribing to our newsletter!', 'success')
    return redirect(request.referrer or url_for('index'))

with app.app_context():
    # Make sure to import the models here or their tables won't be created
    import models  # noqa: F401
    db.create_all()
