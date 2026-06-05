import logging
from flask import render_template, request, redirect, url_for, flash


def register_routes(app):
    """Register all application routes"""
    from app import db

    # Import models with error handling
    try:
        from models import Appointment, ContactMessage, Newsletter
        MODELS_AVAILABLE = True
    except Exception as e:
        app.logger.warning(f"Models not available: {e}")
        MODELS_AVAILABLE = False

    from forms import AppointmentForm, ContactForm, NewsletterForm

    # ------------------------------------------------------------------ #
    #  Page Routes
    # ------------------------------------------------------------------ #

    @app.route('/')
    @app.route('/home')
    def index():
        return render_template('index.html', newsletter_form=NewsletterForm())

    @app.route('/about')
    def about():
        return render_template('about.html', newsletter_form=NewsletterForm())

    @app.route('/departments')
    def departments():
        return render_template('departments.html', newsletter_form=NewsletterForm())

    @app.route('/doctors')
    def doctors():
        return render_template('doctors.html', newsletter_form=NewsletterForm())

    @app.route('/patient-care')
    def patient_care():
        return render_template('patient_care.html', newsletter_form=NewsletterForm())

    @app.route('/testimonials')
    def testimonials():
        return render_template('testimonials.html', newsletter_form=NewsletterForm())

    @app.route('/blog')
    def blog():
        return render_template('blog.html', newsletter_form=NewsletterForm())

    @app.route('/careers')
    def careers():
        return render_template('careers.html', newsletter_form=NewsletterForm())

    @app.route('/news')
    def news():
        return render_template('news.html', newsletter_form=NewsletterForm())

    # ------------------------------------------------------------------ #
    #  Form Routes
    # ------------------------------------------------------------------ #

    @app.route('/appointment', methods=['GET', 'POST'])
    def appointment():
        form = AppointmentForm()
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
                        message=form.message.data,
                    )
                    db.session.add(new_appointment)
                    db.session.commit()
                    flash('Appointment booked successfully! We will contact you soon.', 'success')
                except Exception as e:
                    db.session.rollback()
                    logging.error(f"Error booking appointment: {e}")
                    flash('Error booking appointment. Please try again.', 'danger')
            else:
                flash('Appointment request received! We will connect you soon.', 'info')
            return redirect(url_for('appointment'))

        return render_template('appointment.html', form=form, newsletter_form=NewsletterForm())

    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        form = ContactForm()
        if form.validate_on_submit():
            if MODELS_AVAILABLE:
                try:
                    new_message = ContactMessage(
                        name=form.name.data,
                        email=form.email.data,
                        subject=form.subject.data,
                        message=form.message.data,
                    )
                    db.session.add(new_message)
                    db.session.commit()
                    flash('Message sent successfully! We will get back to you soon.', 'success')
                except Exception as e:
                    db.session.rollback()
                    logging.error(f"Error sending contact message: {e}")
                    flash('Error sending message. Please try again.', 'danger')
            else:
                flash('Message received! We will get back to you soon.', 'info')
            return redirect(url_for('contact'))

        return render_template('contact.html', form=form, newsletter_form=NewsletterForm())

    @app.route('/newsletter-subscribe', methods=['POST'])
    def newsletter_subscribe():
        form = NewsletterForm()
        if form.validate_on_submit():
            if MODELS_AVAILABLE:
                try:
                    existing = Newsletter.query.filter_by(email=form.email.data).first()
                    if existing:
                        flash('This email is already subscribed.', 'info')
                    else:
                        db.session.add(Newsletter(email=form.email.data))
                        db.session.commit()
                        flash('Thank you for subscribing!', 'success')
                except Exception as e:
                    db.session.rollback()
                    logging.error(f"Newsletter subscription error: {e}")
                    flash('Subscription error. Please try again.', 'danger')
            else:
                flash('Subscription received!', 'info')

        return redirect(request.referrer or url_for('index'))

    # ------------------------------------------------------------------ #
    #  Error Handlers
    # ------------------------------------------------------------------ #

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html', newsletter_form=NewsletterForm()), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html', newsletter_form=NewsletterForm()), 500
