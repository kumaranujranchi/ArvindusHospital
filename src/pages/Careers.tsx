import React from 'react';
import { Container, Row, Col, Card } from 'react-bootstrap';

const Careers: React.FC = () => {
  const jobOpenings = [
    {
      title: 'Staff Nurse',
      department: 'Nursing',
      location: 'Patna',
      type: 'Full-time'
    },
    {
      title: 'Medical Technologist',
      department: 'Laboratory',
      location: 'Chapra',
      type: 'Full-time'
    },
    {
      title: 'Physiotherapist',
      department: 'Rehabilitation',
      location: 'Jamui',
      type: 'Part-time'
    }
  ];

  return (
    <div className="page-content">
      <Container>
        <Row>
          <Col lg={12}>
            <div className="page-header">
              <h1>Career Opportunities</h1>
              <p className="lead">
                Join our team of dedicated healthcare professionals.
              </p>
            </div>
          </Col>
        </Row>
        
        <Row className="mt-5">
          <Col lg={8}>
            <h2>Current Openings</h2>
            {jobOpenings.map((job, index) => (
              <Card key={index} className="mb-3">
                <Card.Body>
                  <Row>
                    <Col md={8}>
                      <Card.Title>{job.title}</Card.Title>
                      <p className="mb-1"><strong>Department:</strong> {job.department}</p>
                      <p className="mb-1"><strong>Location:</strong> {job.location}</p>
                      <p className="mb-0"><strong>Type:</strong> {job.type}</p>
                    </Col>
                    <Col md={4} className="text-end">
                      <button className="btn btn-primary">Apply Now</button>
                    </Col>
                  </Row>
                </Card.Body>
              </Card>
            ))}
          </Col>
          <Col lg={4}>
            <Card>
              <Card.Body>
                <Card.Title>Why Work With Us?</Card.Title>
                <ul>
                  <li>Competitive salary packages</li>
                  <li>Professional development opportunities</li>
                  <li>Modern work environment</li>
                  <li>Health insurance benefits</li>
                  <li>Work-life balance</li>
                </ul>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default Careers;
