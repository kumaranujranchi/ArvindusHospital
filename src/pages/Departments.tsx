import React from 'react';
import { Container, Row, Col, Card } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const Departments: React.FC = () => {
  const departments = [
    {
      name: 'Cardiology',
      icon: 'fas fa-heartbeat',
      description: 'Comprehensive heart care with advanced diagnostic and treatment facilities for all cardiac conditions.',
      services: ['ECG', 'Echocardiography', 'Cardiac Catheterization', 'Angioplasty']
    },
    {
      name: 'Neurology',
      icon: 'fas fa-brain',
      description: 'Expert diagnosis and treatment of disorders of the nervous system, brain, and spinal cord.',
      services: ['EEG', 'MRI Brain', 'Stroke Treatment', 'Epilepsy Management']
    },
    {
      name: 'Orthopedics',
      icon: 'fas fa-user-md',
      description: 'Advanced orthopedic care for bone, joint, and muscle conditions with minimally invasive techniques.',
      services: ['Joint Replacement', 'Arthroscopy', 'Fracture Treatment', 'Sports Medicine']
    },
    {
      name: 'Pediatrics',
      icon: 'fas fa-baby',
      description: 'Specialized healthcare for infants, children, and adolescents with child-friendly environment.',
      services: ['Vaccination', 'Growth Monitoring', 'Pediatric Surgery', 'Neonatal Care']
    },
    {
      name: 'Gynecology',
      icon: 'fas fa-female',
      description: 'Comprehensive women\'s health services including maternity care and gynecological treatments.',
      services: ['Prenatal Care', 'Delivery', 'Gynecological Surgery', 'Family Planning']
    },
    {
      name: 'Ophthalmology',
      icon: 'fas fa-eye',
      description: 'Advanced eye care services including cataract surgery, retinal treatments, and vision correction.',
      services: ['Cataract Surgery', 'Retinal Treatment', 'LASIK', 'Glaucoma Treatment']
    },
    {
      name: 'General Medicine',
      icon: 'fas fa-stethoscope',
      description: 'Primary healthcare services for diagnosis and treatment of common medical conditions.',
      services: ['Health Checkups', 'Chronic Disease Management', 'Preventive Care', 'Consultation']
    },
    {
      name: 'Surgery',
      icon: 'fas fa-cut',
      description: 'Advanced surgical procedures with state-of-the-art operation theaters and expert surgeons.',
      services: ['General Surgery', 'Laparoscopic Surgery', 'Emergency Surgery', 'Day Care Surgery']
    },
    {
      name: 'Emergency Medicine',
      icon: 'fas fa-ambulance',
      description: '24/7 emergency care with immediate medical attention for critical and urgent conditions.',
      services: ['Trauma Care', 'Critical Care', 'Emergency Surgery', 'Ambulance Service']
    }
  ];

  return (
    <div className="page-content">
      <Container>
        <Row>
          <Col lg={12}>
            <div className="page-header">
              <h1>Departments & Specialties</h1>
              <p className="lead">
                Comprehensive medical services across multiple specialties with expert healthcare professionals.
              </p>
            </div>
          </Col>
        </Row>
        
        <Row className="mt-5">
          {departments.map((dept, index) => (
            <Col lg={4} md={6} key={index} className="mb-4">
              <Card className="h-100 department-card">
                <Card.Body>
                  <div className="department-icon text-center mb-3">
                    <i className={dept.icon}></i>
                  </div>
                  <Card.Title className="text-center">{dept.name}</Card.Title>
                  <Card.Text>{dept.description}</Card.Text>
                  
                  <h6>Services:</h6>
                  <ul className="services-list">
                    {dept.services.map((service, idx) => (
                      <li key={idx}>{service}</li>
                    ))}
                  </ul>
                  
                  <div className="text-center mt-3">
                    <Link to="/appointment" className="btn btn-outline-primary">
                      Book Appointment
                    </Link>
                  </div>
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>
      </Container>
    </div>
  );
};

export default Departments;
