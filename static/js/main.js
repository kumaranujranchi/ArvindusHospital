document.addEventListener('DOMContentLoaded', function() {
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
});
