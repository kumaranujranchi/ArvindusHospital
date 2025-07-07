import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';

const PatientCare: React.FC = () => {
  return (
    <div className="page-content">
      <Container>
        <Row>
          <Col lg={12}>
            <div className="page-header">
              <h1>Patient Care</h1>
              <p className="lead">
                Comprehensive patient care services designed for your comfort and recovery.
              </p>
            </div>
          </Col>
        </Row>
        
        <Row className="mt-5">
          <Col lg={6}>
            <h2>Our Patient Care Philosophy</h2>
            <p>
              At Arvindu Hospitals, we believe that exceptional patient care goes beyond medical treatment. 
              We focus on providing a holistic healing environment that addresses not just your physical 
              health, but also your emotional and psychological well-being.
            </p>
            
            <h3>What We Offer:</h3>
            <ul>
              <li>24/7 nursing care</li>
              <li>Patient education and counseling</li>
              <li>Nutritional guidance</li>
              <li>Rehabilitation services</li>
              <li>Discharge planning</li>
              <li>Follow-up care</li>
            </ul>
          </Col>
          <Col lg={6}>
            <img 
              src="/images/patient-care.png" 
              alt="Patient Care" 
              className="img-fluid rounded"
            />
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default PatientCare;
