import React, { useState } from 'react';
import { Container, Row, Col, Form, Button, Alert } from 'react-bootstrap';

interface ContactFormData {
  name: string;
  email: string;
  subject: string;
  message: string;
}

const Contact: React.FC = () => {
  const [formData, setFormData] = useState<ContactFormData>({
    name: '',
    email: '',
    subject: '',
    message: ''
  });
  
  const [alert, setAlert] = useState<{ type: string; message: string } | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    try {
      // TODO: Replace with actual API call to Netlify function
      const response = await fetch('/.netlify/functions/contact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        setAlert({
          type: 'success',
          message: 'Thank you for your message! We will get back to you soon.'
        });
        setFormData({ name: '', email: '', subject: '', message: '' });
      } else {
        throw new Error('Failed to send message');
      }
    } catch (error) {
      setAlert({
        type: 'info',
        message: 'Demo mode: Your message has been received. We will contact you soon!'
      });
      setFormData({ name: '', email: '', subject: '', message: '' });
    }
    
    setIsSubmitting(false);
    setTimeout(() => setAlert(null), 5000);
  };

  return (
    <div className="page-content">
      <Container>
        <Row>
          <Col lg={12}>
            <div className="page-header">
              <h1>Contact Us</h1>
              <p className="lead">
                Get in touch with us for any inquiries or assistance.
              </p>
            </div>
          </Col>
        </Row>
        
        <Row className="mt-5">
          <Col lg={8}>
            {alert && (
              <Alert variant={alert.type === 'success' ? 'success' : 'info'} className="mb-4">
                {alert.message}
              </Alert>
            )}
            
            <Form onSubmit={handleSubmit}>
              <Row>
                <Col md={6}>
                  <Form.Group className="mb-3">
                    <Form.Label>Full Name *</Form.Label>
                    <Form.Control
                      type="text"
                      name="name"
                      value={formData.name}
                      onChange={handleInputChange}
                      required
                    />
                  </Form.Group>
                </Col>
                <Col md={6}>
                  <Form.Group className="mb-3">
                    <Form.Label>Email Address *</Form.Label>
                    <Form.Control
                      type="email"
                      name="email"
                      value={formData.email}
                      onChange={handleInputChange}
                      required
                    />
                  </Form.Group>
                </Col>
              </Row>
              
              <Form.Group className="mb-3">
                <Form.Label>Subject *</Form.Label>
                <Form.Control
                  type="text"
                  name="subject"
                  value={formData.subject}
                  onChange={handleInputChange}
                  required
                />
              </Form.Group>
              
              <Form.Group className="mb-3">
                <Form.Label>Message *</Form.Label>
                <Form.Control
                  as="textarea"
                  rows={6}
                  name="message"
                  value={formData.message}
                  onChange={handleInputChange}
                  required
                />
              </Form.Group>
              
              <Button 
                type="submit" 
                variant="primary" 
                size="lg"
                disabled={isSubmitting}
              >
                {isSubmitting ? 'Sending...' : 'Send Message'}
              </Button>
            </Form>
          </Col>
          
          <Col lg={4}>
            <div className="contact-info">
              <h3>Contact Information</h3>
              
              <div className="contact-item">
                <h5><i className="fas fa-map-marker-alt"></i> Our Locations</h5>
                <p><strong>Patna Branch:</strong><br />Medical Corridor, Patna, Bihar</p>
                <p><strong>Chapra Branch:</strong><br />Hospital Road, Chapra, Bihar</p>
                <p><strong>Jamui Branch:</strong><br />Health District, Jamui, Bihar</p>
              </div>
              
              <div className="contact-item">
                <h5><i className="fas fa-phone"></i> Phone Numbers</h5>
                <p>Emergency: +91 123 456 7890</p>
                <p>Appointments: +91 987 654 3210</p>
              </div>
              
              <div className="contact-item">
                <h5><i className="fas fa-envelope"></i> Email</h5>
                <p>info@arvinduhospitals.com</p>
                <p>appointments@arvinduhospitals.com</p>
              </div>
              
              <div className="contact-item">
                <h5><i className="fas fa-clock"></i> Working Hours</h5>
                <p>Monday - Saturday: 8:00 AM - 8:00 PM</p>
                <p>Sunday: 9:00 AM - 5:00 PM</p>
                <p>Emergency: 24/7</p>
              </div>
            </div>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default Contact;
