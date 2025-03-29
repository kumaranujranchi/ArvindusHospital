from flask import render_template, request, redirect, url_for, flash
from app import app, db
from forms import AppointmentForm, ContactForm, NewsletterForm
from models import Appointment, ContactMessage, Newsletter
import logging


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


@app.route('/doctors')
def doctors():
    newsletter_form = NewsletterForm()
    return render_template('doctors.html', newsletter_form=newsletter_form)


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


@app.route('/news')
def news():
    newsletter_form = NewsletterForm()
    return render_template('news.html', newsletter_form=newsletter_form)


@app.route('/csr')
def csr():
    newsletter_form = NewsletterForm()
    return render_template('csr.html', newsletter_form=newsletter_form)


@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    form = AppointmentForm()
    newsletter_form = NewsletterForm()
    
    if form.validate_on_submit():
        try:
            new_appointment = Appointment(
                name=form.name.data,
                email=form.email.data,
                phone=form.phone.data,
                department=form.department.data,
                doctor=form.doctor.data,
                date=form.date.data,
                time=form.time.data,
                message=form.message.data
            )
            db.session.add(new_appointment)
            db.session.commit()
            flash('Your appointment has been booked successfully! We will contact you soon.', 'success')
            return redirect(url_for('appointment'))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error booking appointment: {e}")
            flash('There was an error booking your appointment. Please try again.', 'danger')
    
    return render_template('appointment.html', form=form, newsletter_form=newsletter_form)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    newsletter_form = NewsletterForm()
    
    if form.validate_on_submit():
        try:
            new_message = ContactMessage(
                name=form.name.data,
                email=form.email.data,
                subject=form.subject.data,
                message=form.message.data
            )
            db.session.add(new_message)
            db.session.commit()
            flash('Your message has been sent successfully! We will get back to you soon.', 'success')
            return redirect(url_for('contact'))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error sending contact message: {e}")
            flash('There was an error sending your message. Please try again.', 'danger')
    
    return render_template('contact.html', form=form, newsletter_form=newsletter_form)


@app.route('/newsletter-subscribe', methods=['POST'])
def newsletter_subscribe():
    form = NewsletterForm()
    
    if form.validate_on_submit():
        try:
            # Check if email already exists
            existing_email = Newsletter.query.filter_by(email=form.email.data).first()
            if existing_email:
                flash('This email is already subscribed to our newsletter.', 'info')
            else:
                new_subscriber = Newsletter(email=form.email.data)
                db.session.add(new_subscriber)
                db.session.commit()
                flash('Thank you for subscribing to our newsletter!', 'success')
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error subscribing to newsletter: {e}")
            flash('There was an error processing your subscription. Please try again.', 'danger')
    
    # Redirect back to the referring page
    return redirect(request.referrer or url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    newsletter_form = NewsletterForm()
    return render_template('404.html', newsletter_form=newsletter_form), 404


@app.errorhandler(500)
def server_error(e):
    newsletter_form = NewsletterForm()
    return render_template('500.html', newsletter_form=newsletter_form), 500
