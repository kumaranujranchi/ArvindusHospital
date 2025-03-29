/**
 * Arvindu Hospitals - Main JavaScript
 * A professional, modern hospital website
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Handle navbar scroll behavior
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        });
    }

    // Initialize testimonial slider if it exists
    const testimonialSlider = document.querySelector('.testimonial-slider');
    if (testimonialSlider && typeof $.fn.slick !== 'undefined') {
        $('.testimonial-slider').slick({
            dots: true,
            infinite: true,
            speed: 500,
            slidesToShow: 3,
            slidesToScroll: 1,
            autoplay: true,
            autoplaySpeed: 5000,
            arrows: false,
            responsive: [
                {
                    breakpoint: 992,
                    settings: {
                        slidesToShow: 2
                    }
                },
                {
                    breakpoint: 768,
                    settings: {
                        slidesToShow: 1
                    }
                }
            ]
        });
    }

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    if (forms.length > 0) {
        Array.from(forms).forEach(form => {
            form.addEventListener('submit', event => {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }

    // Dynamic year in footer copyright
    const yearElement = document.querySelector('.current-year');
    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a.smooth-scroll').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            
            if (targetId.startsWith('#') && targetId.length > 1) {
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    window.scrollTo({
                        top: targetElement.offsetTop - 80,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });

    // Department filter
    const departmentFilter = document.getElementById('department-filter');
    if (departmentFilter) {
        departmentFilter.addEventListener('change', function() {
            const selectedDepartment = this.value;
            const doctorCards = document.querySelectorAll('.doctor-card');
            
            doctorCards.forEach(card => {
                if (selectedDepartment === 'all' || card.getAttribute('data-department') === selectedDepartment) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }

    // Blog filter
    const blogFilter = document.getElementById('blog-filter');
    if (blogFilter) {
        blogFilter.addEventListener('change', function() {
            const selectedCategory = this.value;
            const blogCards = document.querySelectorAll('.blog-card');
            
            blogCards.forEach(card => {
                if (selectedCategory === 'all' || card.getAttribute('data-category') === selectedCategory) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }

    // Toggle accordion items
    const accordionHeaders = document.querySelectorAll('.accordion-header');
    if (accordionHeaders.length > 0) {
        accordionHeaders.forEach(header => {
            header.addEventListener('click', function() {
                const accordionItem = this.parentElement;
                accordionItem.classList.toggle('active');
                
                const accordionContent = this.nextElementSibling;
                if (accordionItem.classList.contains('active')) {
                    accordionContent.style.maxHeight = accordionContent.scrollHeight + 'px';
                } else {
                    accordionContent.style.maxHeight = null;
                }
            });
        });
    }

    // Dynamic appointment form
    const departmentSelect = document.getElementById('department');
    const doctorSelect = document.getElementById('doctor');
    
    if (departmentSelect && doctorSelect) {
        const mockDoctorData = {
            'cardiology': ['Dr. Sharma', 'Dr. Gupta'],
            'neurology': ['Dr. Patel', 'Dr. Singh'],
            'orthopedics': ['Dr. Kumar', 'Dr. Verma'],
            'pediatrics': ['Dr. Mishra', 'Dr. Roy'],
            'ophthalmology': ['Dr. Jain', 'Dr. Das'],
            'dermatology': ['Dr. Reddy', 'Dr. Shah'],
            'gynecology': ['Dr. Bose', 'Dr. Kapoor'],
            'urology': ['Dr. Ahmed', 'Dr. Rao'],
            'ent': ['Dr. Naidu', 'Dr. Nair'],
            'dental': ['Dr. Mehta', 'Dr. Khanna']
        };
        
        departmentSelect.addEventListener('change', function() {
            const selectedDepartment = this.value;
            
            // Clear existing options
            doctorSelect.innerHTML = '<option value="">Select Doctor</option>';
            doctorSelect.innerHTML += '<option value="any">Any Doctor</option>';
            
            // Add department-specific doctors if department is selected
            if (selectedDepartment && selectedDepartment !== '' && mockDoctorData[selectedDepartment]) {
                mockDoctorData[selectedDepartment].forEach(doctor => {
                    const option = document.createElement('option');
                    option.value = doctor.toLowerCase().replace(' ', '-');
                    option.textContent = doctor;
                    doctorSelect.appendChild(option);
                });
            }
        });
    }
});
