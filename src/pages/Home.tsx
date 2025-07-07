import React from 'react';
import { Container, Row, Col, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const Home: React.FC = () => {
  return (
    <>
      {/* Hero Section */}
      <section className="hero-section">
        <Container>
          <Row>
            <Col lg={12} className="text-center">
              <h1>World-Class Healthcare at Your Fingertips</h1>
              <p>
                Arvindu Hospitals is a premier multispecialty healthcare network based in Bihar, 
                committed to delivering world-class medical services with a compassionate touch. 
                As a reputed hospital brand with branches in Patna, Chapra, and a new facility 
                coming up in Jamui, we bring advanced healthcare infrastructure and expert medical 
                professionals to the region.
              </p>
              <div className="hero-btns">
                <Link to="/appointment" className="btn btn-light">
                  Book Appointment
                </Link>
                <Link to="/doctors" className="btn btn-outline-light">
                  Find a Doctor
                </Link>
              </div>
            </Col>
          </Row>
        </Container>
      </section>

      {/* Services/Departments Section */}
      <section className="section-padding">
        <Container>
          <div className="section-title">
            <h2>Our Specialties</h2>
            <p>
              Arvindu Hospitals offers a wide range of specialized medical services with 
              state-of-the-art technology and expert healthcare professionals.
            </p>
          </div>
          <Row>
            <Col lg={4} md={6}>
              <div className="service-box">
                <div className="service-icon">
                  <i className="fas fa-heartbeat"></i>
                </div>
                <h3>Cardiology</h3>
                <p>
                  Comprehensive heart care with advanced diagnostic and treatment facilities 
                  for all cardiac conditions.
                </p>
                <Link to="/departments" className="btn btn-outline-primary mt-3">
                  Learn More
                </Link>
              </div>
            </Col>
            <Col lg={4} md={6}>
              <div className="service-box">
                <div className="service-icon">
                  <i className="fas fa-brain"></i>
                </div>
                <h3>Neurology</h3>
                <p>
                  Expert diagnosis and treatment of disorders of the nervous system, 
                  brain, and spinal cord.
                </p>
                <Link to="/departments" className="btn btn-outline-primary mt-3">
                  Learn More
                </Link>
              </div>
            </Col>
            <Col lg={4} md={6}>
              <div className="service-box">
                <div className="service-icon">
                  <i className="fas fa-user-md"></i>
                </div>
                <h3>Orthopedics</h3>
                <p>
                  Advanced orthopedic care for bone, joint, and muscle conditions with 
                  minimally invasive techniques.
                </p>
                <Link to="/departments" className="btn btn-outline-primary mt-3">
                  Learn More
                </Link>
              </div>
            </Col>
            <Col lg={4} md={6}>
              <div className="service-box">
                <div className="service-icon">
                  <i className="fas fa-baby"></i>
                </div>
                <h3>Pediatrics</h3>
                <p>
                  Specialized healthcare for infants, children, and adolescents with 
                  child-friendly environment.
                </p>
                <Link to="/departments" className="btn btn-outline-primary mt-3">
                  Learn More
                </Link>
              </div>
            </Col>
            <Col lg={4} md={6}>
              <div className="service-box">
                <div className="service-icon">
                  <i className="fas fa-female"></i>
                </div>
                <h3>Gynecology</h3>
                <p>
                  Comprehensive women's health services including maternity care and 
                  gynecological treatments.
                </p>
                <Link to="/departments" className="btn btn-outline-primary mt-3">
                  Learn More
                </Link>
              </div>
            </Col>
            <Col lg={4} md={6}>
              <div className="service-box">
                <div className="service-icon">
                  <i className="fas fa-eye"></i>
                </div>
                <h3>Ophthalmology</h3>
                <p>
                  Advanced eye care services including cataract surgery, retinal treatments, 
                  and vision correction.
                </p>
                <Link to="/departments" className="btn btn-outline-primary mt-3">
                  Learn More
                </Link>
              </div>
            </Col>
          </Row>
        </Container>
      </section>

      {/* Why Choose Us Section */}
      <section className="section-padding bg-light">
        <Container>
          <div className="section-title">
            <h2>Why Choose Arvindu Hospitals?</h2>
            <p>
              We are committed to providing exceptional healthcare services that prioritize 
              patient safety, comfort, and recovery.
            </p>
          </div>
          <Row>
            <Col lg={3} md={6} className="mb-4">
              <div className="feature-box text-center">
                <div className="feature-icon">
                  <i className="fas fa-award"></i>
                </div>
                <h4>Expert Medical Team</h4>
                <p>
                  Highly qualified and experienced doctors and medical professionals 
                  dedicated to your health.
                </p>
              </div>
            </Col>
            <Col lg={3} md={6} className="mb-4">
              <div className="feature-box text-center">
                <div className="feature-icon">
                  <i className="fas fa-hospital"></i>
                </div>
                <h4>State-of-the-Art Facilities</h4>
                <p>
                  Modern medical equipment and advanced technology for accurate diagnosis 
                  and effective treatment.
                </p>
              </div>
            </Col>
            <Col lg={3} md={6} className="mb-4">
              <div className="feature-box text-center">
                <div className="feature-icon">
                  <i className="fas fa-clock"></i>
                </div>
                <h4>24/7 Emergency Care</h4>
                <p>
                  Round-the-clock emergency services with immediate medical attention 
                  when you need it most.
                </p>
              </div>
            </Col>
            <Col lg={3} md={6} className="mb-4">
              <div className="feature-box text-center">
                <div className="feature-icon">
                  <i className="fas fa-heart"></i>
                </div>
                <h4>Compassionate Care</h4>
                <p>
                  Patient-centered approach with personalized care and emotional support 
                  throughout your treatment.
                </p>
              </div>
            </Col>
          </Row>
        </Container>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <Container>
          <Row>
            <Col lg={8} className="mx-auto text-center">
              <h2>Ready to Experience World-Class Healthcare?</h2>
              <p>
                Book your appointment today and take the first step towards better health 
                with Arvindu Hospitals.
              </p>
              <div className="cta-buttons">
                <Link to="/appointment" className="btn btn-light btn-lg me-3">
                  Book Appointment
                </Link>
                <Link to="/contact" className="btn btn-outline-light btn-lg">
                  Contact Us
                </Link>
              </div>
            </Col>
          </Row>
        </Container>
      </section>
    </>
  );
};

export default Home;
