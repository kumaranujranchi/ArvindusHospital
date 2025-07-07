// Custom Cursor
document.addEventListener('DOMContentLoaded', function() {
    // Create and append custom cursor
    const cursor = document.createElement('div');
    cursor.classList.add('custom-cursor');
    document.body.appendChild(cursor);

    // Update cursor position on mouse movement
    document.addEventListener('mousemove', function(e) {
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
    });

    // Add hover effect for interactive elements
    const interactiveElements = document.querySelectorAll('a, button, input, textarea, select, .btn, .nav-link, .card, .service-box, .blog-card, .doctor-card');
    
    interactiveElements.forEach(function(element) {
        element.addEventListener('mouseenter', function() {
            cursor.classList.add('hover');
        });
        
        element.addEventListener('mouseleave', function() {
            cursor.classList.remove('hover');
        });
    });
    
    // Replace blue colors with theme colors
    
    // Fix department card headers
    const departmentHeaders = document.querySelectorAll('.department-item .card-header');
    departmentHeaders.forEach(header => {
        header.classList.remove('bg-primary');
        header.style.backgroundColor = 'var(--primary-color)';
        
        // Make header text peach/coral color
        const headerTitle = header.querySelector('h3');
        if (headerTitle) {
            headerTitle.style.color = 'var(--secondary-color)';
        }
        
        // Make icons peach/coral color
        const headerIcon = header.querySelector('i');
        if (headerIcon) {
            headerIcon.style.color = 'var(--secondary-color)';
        }
    });
    
    // Fix doctor icons
    const doctorIcons = document.querySelectorAll('.fas.fa-user-md');
    doctorIcons.forEach(icon => {
        icon.classList.remove('text-primary');
        icon.style.color = 'var(--secondary-color)';
    });
    
    // Fix blog buttons
    const blogButtons = document.querySelectorAll('.btn-outline-primary, .btn-primary');
    blogButtons.forEach(button => {
        if (button.classList.contains('btn-outline-primary')) {
            button.classList.remove('btn-outline-primary');
            button.classList.add('btn-outline-secondary');
        }
        else if (button.classList.contains('btn-primary') && !button.classList.contains('appointment-btn')) {
            button.classList.remove('btn-primary');
            button.classList.add('btn-secondary');
        }
    });
    // Initialize Slick Slider for testimonials
    if (document.querySelector('.testimonial-slider')) {
        $('.testimonial-slider').slick({
            dots: true,
            infinite: true,
            speed: 500,
            slidesToShow: 3,
            slidesToScroll: 1,
            autoplay: true,
            autoplaySpeed: 5000,
            responsive: [
                {
                    breakpoint: 992,
                    settings: {
                        slidesToShow: 2,
                        slidesToScroll: 1
                    }
                },
                {
                    breakpoint: 768,
                    settings: {
                        slidesToShow: 1,
                        slidesToScroll: 1
                    }
                }
            ]
        });
    }

    // Sticky Navbar
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('shadow-sm');
            } else {
                navbar.classList.remove('shadow-sm');
            }
        });
    }

    // Department dropdown toggle
    const departmentItems = document.querySelectorAll('.department-item');
    if (departmentItems.length > 0) {
        departmentItems.forEach(item => {
            item.addEventListener('click', function() {
                const content = this.querySelector('.department-content');
                if (content) {
                    const isActive = this.classList.contains('active');
                    
                    // Close all open departments
                    document.querySelectorAll('.department-item.active').forEach(activeItem => {
                        activeItem.classList.remove('active');
                        activeItem.querySelector('.department-content').style.maxHeight = null;
                    });
                    
                    // If the clicked department wasn't active before, open it
                    if (!isActive) {
                        this.classList.add('active');
                        content.style.maxHeight = content.scrollHeight + "px";
                    }
                }
            });
        });
    }

    // Form validation
    const validateForm = (formId) => {
        const form = document.getElementById(formId);
        if (!form) return;

        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    };

    validateForm('appointmentForm');
    validateForm('contactForm');
    validateForm('newsletterForm');

    // Bootstrap Tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    if (tooltipTriggerList.length > 0) {
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Date picker - set min date to today
    const dateInputs = document.querySelectorAll('input[type="date"]');
    if (dateInputs.length > 0) {
        const today = new Date();
        const dd = String(today.getDate()).padStart(2, '0');
        const mm = String(today.getMonth() + 1).padStart(2, '0'); // January is 0!
        const yyyy = today.getFullYear();
        const currentDate = yyyy + '-' + mm + '-' + dd;
        
        dateInputs.forEach(input => {
            input.min = currentDate;
        });
    }

    // Dynamic doctor loading based on department selection
    const departmentSelect = document.getElementById('department');
    const doctorSelect = document.getElementById('doctor');
    
    if (departmentSelect && doctorSelect) {
        departmentSelect.addEventListener('change', function() {
            const department = this.value;
            
            // Clear current options
            doctorSelect.innerHTML = '<option value="">Select Doctor (Optional)</option>';
            
            // Add department-specific doctors
            if (department) {
                const doctors = {
                    'cardiology': [
                        {id: 'dr_sharma', name: 'Dr. Sharma'},
                        {id: 'dr_patel', name: 'Dr. Patel'}
                    ],
                    'neurology': [
                        {id: 'dr_singh', name: 'Dr. Singh'},
                        {id: 'dr_gupta', name: 'Dr. Gupta'}
                    ],
                    'orthopedics': [
                        {id: 'dr_kumar', name: 'Dr. Kumar'},
                        {id: 'dr_verma', name: 'Dr. Verma'}
                    ],
                    'pediatrics': [
                        {id: 'dr_joshi', name: 'Dr. Joshi'},
                        {id: 'dr_reddy', name: 'Dr. Reddy'}
                    ],
                    'gynecology': [
                        {id: 'dr_mishra', name: 'Dr. Mishra'},
                        {id: 'dr_shah', name: 'Dr. Shah'}
                    ],
                    'dermatology': [
                        {id: 'dr_kapoor', name: 'Dr. Kapoor'}
                    ],
                    'ophthalmology': [
                        {id: 'dr_roy', name: 'Dr. Roy'}
                    ],
                    'ent': [
                        {id: 'dr_das', name: 'Dr. Das'}
                    ],
                    'gastroenterology': [
                        {id: 'dr_tiwari', name: 'Dr. Tiwari'}
                    ],
                    'oncology': [
                        {id: 'dr_khan', name: 'Dr. Khan'}
                    ]
                };
                
                if (doctors[department]) {
                    doctors[department].forEach(doctor => {
                        const option = document.createElement('option');
                        option.value = doctor.id;
                        option.textContent = doctor.name;
                        doctorSelect.appendChild(option);
                    });
                }
            }
        });
    }

    // Show flash messages with auto-dismiss
    const flashMessages = document.querySelectorAll('.alert-dismissible');
    if (flashMessages.length > 0) {
        flashMessages.forEach(message => {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(message);
                bsAlert.close();
            }, 5000);
        });
    }

    // Form submission handlers for Netlify Functions

    // Appointment Form Handler
    const appointmentForm = document.getElementById('appointmentForm');
    if (appointmentForm) {
        appointmentForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;

            // Show loading state
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Booking...';

            try {
                const formData = new FormData(this);
                const data = Object.fromEntries(formData.entries());

                const response = await fetch('/.netlify/functions/appointment', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });

                const result = await response.json();

                if (response.ok) {
                    showMessage('success', result.message);
                    this.reset();
                } else {
                    showMessage('error', result.error || 'Failed to book appointment');
                }
            } catch (error) {
                console.error('Error:', error);
                showMessage('error', 'Network error. Please try again.');
            } finally {
                // Reset button state
                submitBtn.disabled = false;
                submitBtn.textContent = originalText;
            }
        });
    }

    // Contact Form Handler
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;

            // Show loading state
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';

            try {
                const formData = new FormData(this);
                const data = Object.fromEntries(formData.entries());

                const response = await fetch('/.netlify/functions/contact', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });

                const result = await response.json();

                if (response.ok) {
                    showMessage('success', result.message);
                    this.reset();
                } else {
                    showMessage('error', result.error || 'Failed to send message');
                }
            } catch (error) {
                console.error('Error:', error);
                showMessage('error', 'Network error. Please try again.');
            } finally {
                // Reset button state
                submitBtn.disabled = false;
                submitBtn.textContent = originalText;
            }
        });
    }

    // Newsletter Form Handler
    const newsletterForm = document.getElementById('newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            const submitBtn = this.querySelector('button[type="submit"]');
            const originalHTML = submitBtn.innerHTML;

            // Show loading state
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';

            try {
                const formData = new FormData(this);
                const data = Object.fromEntries(formData.entries());

                const response = await fetch('/.netlify/functions/newsletter', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });

                const result = await response.json();

                if (response.ok) {
                    showMessage('success', result.message, 'newsletter-message');
                    this.reset();
                } else {
                    showMessage('error', result.error || 'Failed to subscribe', 'newsletter-message');
                }
            } catch (error) {
                console.error('Error:', error);
                showMessage('error', 'Network error. Please try again.', 'newsletter-message');
            } finally {
                // Reset button state
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalHTML;
            }
        });
    }

    // Helper function to show messages
    function showMessage(type, message, targetId = null) {
        const alertClass = type === 'success' ? 'alert-success' : 'alert-danger';
        const iconClass = type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle';

        const alertHTML = `
            <div class="alert ${alertClass} alert-dismissible fade show mt-3" role="alert">
                <i class="fas ${iconClass} me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;

        if (targetId) {
            const target = document.getElementById(targetId);
            if (target) {
                target.innerHTML = alertHTML;
                target.style.display = 'block';
            }
        } else {
            // Show at the top of the page
            const container = document.querySelector('.container');
            if (container) {
                const alertDiv = document.createElement('div');
                alertDiv.innerHTML = alertHTML;
                container.insertBefore(alertDiv, container.firstChild);

                // Auto-dismiss after 5 seconds
                setTimeout(() => {
                    const alert = alertDiv.querySelector('.alert');
                    if (alert) {
                        const bsAlert = new bootstrap.Alert(alert);
                        bsAlert.close();
                    }
                }, 5000);
            }
        }
    }
});
