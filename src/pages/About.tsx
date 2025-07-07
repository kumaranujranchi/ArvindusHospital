import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';

const About: React.FC = () => {
  return (
    <div className="page-content">
      <Container>
        <Row>
          <Col lg={12}>
            <div className="page-header">
              <h1>About Arvindu Hospitals</h1>
              <p className="lead">
                Leading healthcare provider in Bihar, committed to excellence in medical care.
              </p>
            </div>
          </Col>
        </Row>
        
        <Row className="mt-5">
          <Col lg={6}>
            <h2>Our Mission</h2>
            <p>
              To provide world-class healthcare services with compassion, integrity, and excellence. 
              We are committed to improving the health and well-being of our communities through 
              innovative medical care, advanced technology, and a patient-centered approach.
            </p>
            
            <h2 className="mt-4">Our Vision</h2>
            <p>
              To be the most trusted and preferred healthcare provider in Bihar and beyond, 
              setting new standards in medical excellence and patient care.
            </p>
          </Col>
          <Col lg={6}>
            <img 
              src="/images/patient-care.png" 
              alt="Patient Care" 
              className="img-fluid rounded"
            />
          </Col>
        </Row>
        
        <Row className="mt-5">
          <Col lg={12}>
            <h2>Our Values</h2>
            <Row className="mt-4">
              <Col md={4}>
                <div className="value-box">
                  <h4>Compassion</h4>
                  <p>We treat every patient with empathy, kindness, and respect.</p>
                </div>
              </Col>
              <Col md={4}>
                <div className="value-box">
                  <h4>Excellence</h4>
                  <p>We strive for the highest standards in medical care and service.</p>
                </div>
              </Col>
              <Col md={4}>
                <div className="value-box">
                  <h4>Integrity</h4>
                  <p>We maintain honesty and transparency in all our interactions.</p>
                </div>
              </Col>
            </Row>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default About;
