import React from 'react';
import { Container, Row, Col, Card } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const Doctors: React.FC = () => {
  const doctors = [
    {
      name: 'Dr. Rajesh Kumar',
      specialty: 'Cardiology',
      qualification: 'MD, DM (Cardiology)',
      experience: '15+ years',
      image: '/images/doctor-placeholder.jpg'
    },
    {
      name: 'Dr. Priya Sharma',
      specialty: 'Neurology',
      qualification: 'MD, DM (Neurology)',
      experience: '12+ years',
      image: '/images/doctor-placeholder.jpg'
    },
    {
      name: 'Dr. Amit Singh',
      specialty: 'Orthopedics',
      qualification: 'MS (Orthopedics)',
      experience: '18+ years',
      image: '/images/doctor-placeholder.jpg'
    },
    {
      name: 'Dr. Sunita Devi',
      specialty: 'Gynecology',
      qualification: 'MD (Gynecology)',
      experience: '14+ years',
      image: '/images/doctor-placeholder.jpg'
    },
    {
      name: 'Dr. Vikash Gupta',
      specialty: 'Pediatrics',
      qualification: 'MD (Pediatrics)',
      experience: '10+ years',
      image: '/images/doctor-placeholder.jpg'
    },
    {
      name: 'Dr. Neha Verma',
      specialty: 'Ophthalmology',
      qualification: 'MS (Ophthalmology)',
      experience: '8+ years',
      image: '/images/doctor-placeholder.jpg'
    }
  ];

  return (
    <div className="page-content">
      <Container>
        <Row>
          <Col lg={12}>
            <div className="page-header">
              <h1>Find a Doctor</h1>
              <p className="lead">
                Meet our team of experienced and qualified medical professionals.
              </p>
            </div>
          </Col>
        </Row>
        
        <Row className="mt-5">
          {doctors.map((doctor, index) => (
            <Col lg={4} md={6} key={index} className="mb-4">
              <Card className="h-100 doctor-card">
                <div className="doctor-image">
                  <img 
                    src={doctor.image} 
                    alt={doctor.name}
                    onError={(e) => {
                      (e.target as HTMLImageElement).src = 'https://via.placeholder.com/300x300?text=Doctor';
                    }}
                  />
                </div>
                <Card.Body className="text-center">
                  <Card.Title>{doctor.name}</Card.Title>
                  <p className="doctor-specialty">{doctor.specialty}</p>
                  <p className="doctor-qualification">{doctor.qualification}</p>
                  <p className="doctor-experience">Experience: {doctor.experience}</p>
                  
                  <Link to="/appointment" className="btn btn-primary">
                    Book Appointment
                  </Link>
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>
      </Container>
    </div>
  );
};

export default Doctors;
