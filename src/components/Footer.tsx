import React, { useState } from 'react';
import { Container, Row, Col, Form, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const Footer: React.FC = () => {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');

  const handleNewsletterSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      // TODO: Replace with actual API call to Netlify function
      const response = await fetch('/.netlify/functions/newsletter', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      if (response.ok) {
        setMessage('Thank you for subscribing to our newsletter!');
        setEmail('');
      } else {
        setMessage('There was an error. Please try again.');
      }
    } catch (error) {
      setMessage('Demo mode: Newsletter subscription received!');
      setEmail('');
    }

    // Clear message after 3 seconds
    setTimeout(() => setMessage(''), 3000);
  };

  const currentYear = new Date().getFullYear();

  return (
    <footer>
      <Container>
        <Row>
          <Col lg={3} md={6} className="mb-4 mb-lg-0">
            <div className="footer-widget">
              <img 
                src="/images/logo.svg" 
                alt="Arvindu Hospitals Logo" 
                className="mb-4" 
                style={{ height: '50px' }}
              />
              <p>
                Arvindu Hospitals is a multi-specialty healthcare provider committed to 
                providing exceptional medical care with compassion and expertise.
              </p>
              <div className="footer-social mt-4">
                <a href="#" aria-label="Facebook">
                  <i className="fab fa-facebook-f"></i>
                </a>
                <a href="#" aria-label="Twitter">
                  <i className="fab fa-twitter"></i>
                </a>
                <a href="#" aria-label="Instagram">
                  <i className="fab fa-instagram"></i>
                </a>
                <a href="#" aria-label="LinkedIn">
                  <i className="fab fa-linkedin-in"></i>
                </a>
                <a href="#" aria-label="YouTube">
                  <i className="fab fa-youtube"></i>
                </a>
              </div>
            </div>
          </Col>
          
          <Col lg={3} md={6} className="mb-4 mb-lg-0">
            <div className="footer-widget">
              <h3>Quick Links</h3>
              <ul className="footer-links">
                <li><Link to="/about">About Us</Link></li>
                <li><Link to="/departments">Departments & Specialties</Link></li>
                <li><Link to="/doctors">Find a Doctor</Link></li>
                <li><Link to="/patient-care">Patient Care</Link></li>
                <li><Link to="/blog">Health Blog</Link></li>
                <li><Link to="/careers">Career Opportunities</Link></li>
                <li><Link to="/contact">Contact Us</Link></li>
              </ul>
            </div>
          </Col>
          
          <Col lg={3} md={6} className="mb-4 mb-lg-0">
            <div className="footer-widget">
              <h3>Contact Info</h3>
              <ul className="footer-contact-info">
                <li>
                  <i className="fas fa-map-marker-alt"></i>
                  <div>
                    <p><strong>Patna Branch:</strong> Medical Corridor, Patna, Bihar</p>
                    <p><strong>Chapra Branch:</strong> Hospital Road, Chapra, Bihar</p>
                    <p><strong>Jamui Branch:</strong> Health District, Jamui, Bihar</p>
                  </div>
                </li>
                <li>
                  <i className="fas fa-phone-alt"></i>
                  <div>
                    <p>Emergency: +91 123 456 7890</p>
                    <p>Appointments: +91 987 654 3210</p>
                  </div>
                </li>
                <li>
                  <i className="fas fa-envelope"></i>
                  <div>
                    <p>info@arvinduhospitals.com</p>
                    <p>appointments@arvinduhospitals.com</p>
                  </div>
                </li>
              </ul>
            </div>
          </Col>
          
          <Col lg={3} md={6}>
            <div className="footer-widget">
              <h3>Newsletter</h3>
              <div className="footer-newsletter">
                <p>Subscribe to our newsletter to receive health tips, updates, and news.</p>
                <Form onSubmit={handleNewsletterSubmit}>
                  <div className="d-flex">
                    <Form.Control
                      type="email"
                      placeholder="Your Email Address"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      required
                    />
                    <Button type="submit" variant="primary">
                      <i className="fas fa-paper-plane"></i>
                    </Button>
                  </div>
                </Form>
                {message && (
                  <div className="mt-2 text-success small">
                    {message}
                  </div>
                )}
              </div>
            </div>
          </Col>
        </Row>
      </Container>
      
      <div className="footer-bottom">
        <Container>
          <p>&copy; <span className="current-year">{currentYear}</span> Arvindu Hospitals. All Rights Reserved.</p>
        </Container>
      </div>
    </footer>
  );
};

export default Footer;
