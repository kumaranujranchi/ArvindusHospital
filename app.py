import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from config import get_config

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def create_app(config_name=None):
    """Application factory pattern"""
    app = Flask(__name__)

    # Load configuration
    if config_name is None:
        config_class = get_config()
    else:
        from config import config
        config_class = config.get(config_name, config['default'])

    app.config.from_object(config_class)
    config_class.init_app(app)

    # Initialize extensions
    db.init_app(app)

    # Register routes
    register_routes(app)

    # Initialize monitoring and performance optimizations
    if not app.testing:
        from monitoring import init_monitoring
        from performance import init_performance_optimizations

        init_monitoring(app)
        init_performance_optimizations(app)

    return app

def register_routes(app):
    """Register all routes with the app"""
    from flask import render_template, request, redirect, url_for, flash, current_app
    from forms import AppointmentForm, ContactForm, NewsletterForm
    import logging

    # Import models with error handling
    try:
        from models import Appointment, ContactMessage, Newsletter
        MODELS_AVAILABLE = True
    except Exception as e:
        app.logger.warning(f"Models not available: {e}")
        MODELS_AVAILABLE = False

    @app.route('/')
    def index():
        newsletter_form = NewsletterForm()
        return render_template('index.html', newsletter_form=newsletter_form)

    @app.route('/home')
    def home():
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
            if MODELS_AVAILABLE:
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
            else:
                # Database not available - show demo message
                flash('Demo mode: Your appointment request has been received. Database will be connected soon!', 'info')
                logging.info(f"Demo appointment: {form.name.data} - {form.email.data} - {form.department.data}")
                return redirect(url_for('appointment'))

        return render_template('appointment.html', form=form, newsletter_form=newsletter_form)

    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        form = ContactForm()
        newsletter_form = NewsletterForm()

        if form.validate_on_submit():
            if MODELS_AVAILABLE:
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
            else:
                # Database not available - show demo message
                flash('Demo mode: Your message has been received. Database will be connected soon!', 'info')
                logging.info(f"Demo contact: {form.name.data} - {form.email.data} - {form.subject.data}")
                return redirect(url_for('contact'))

        return render_template('contact.html', form=form, newsletter_form=newsletter_form)

    @app.route('/newsletter-subscribe', methods=['POST'])
    def newsletter_subscribe():
        form = NewsletterForm()

        if form.validate_on_submit():
            if MODELS_AVAILABLE:
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
            else:
                # Database not available - show demo message
                flash('Demo mode: Newsletter subscription received. Database will be connected soon!', 'info')
                logging.info(f"Demo newsletter subscription: {form.email.data}")

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

# Create the app instance
app = create_app()

def init_database(app):
    """Initialize database tables if needed"""
    with app.app_context():
        try:
            # Make sure to import the models here or their tables won't be created
            import models  # noqa: F401

            # Only create tables if database is available
            db.create_all()
            app.logger.info("Database tables initialized successfully")
        except Exception as e:
            app.logger.warning(f"Database initialization failed: {e}")
            app.logger.warning("Application will run without database functionality")

# Initialize database for non-serverless environments
if not os.environ.get('NETLIFY'):
    init_database(app)
