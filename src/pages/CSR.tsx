import React from 'react';
import { Container, Row, Col, Card } from 'react-bootstrap';

const CSR: React.FC = () => {
  const initiatives = [
    {
      title: 'Free Health Camps',
      description: 'Regular health screening camps in rural and underserved areas of Bihar.',
      impact: '5000+ people screened annually'
    },
    {
      title: 'Medical Education Support',
      description: 'Scholarships and support for medical students from economically disadvantaged backgrounds.',
      impact: '50+ students supported'
    },
    {
      title: 'Community Health Awareness',
      description: 'Health awareness programs on preventive care, hygiene, and nutrition.',
      impact: '100+ programs conducted'
    }
  ];

  return (
    <div className="page-content">
      <Container>
        <Row>
          <Col lg={12}>
            <div className="page-header">
              <h1>CSR Initiatives</h1>
              <p className="lead">
                Our commitment to giving back to the community through various social responsibility programs.
              </p>
            </div>
          </Col>
        </Row>
        
        <Row className="mt-5">
          {initiatives.map((initiative, index) => (
            <Col lg={4} md={6} key={index} className="mb-4">
              <Card className="h-100 csr-card">
                <Card.Body>
                  <Card.Title>{initiative.title}</Card.Title>
                  <Card.Text>{initiative.description}</Card.Text>
                  <div className="csr-impact">
                    <strong>Impact:</strong> {initiative.impact}
                  </div>
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>
        
        <Row className="mt-5">
          <Col lg={12}>
            <Card>
              <Card.Body>
                <h3>Our CSR Philosophy</h3>
                <p>
                  At Arvindu Hospitals, we believe that healthcare is a fundamental right. Our CSR initiatives 
                  are designed to make quality healthcare accessible to all sections of society, regardless of 
                  their economic status. We are committed to improving the overall health and well-being of 
                  the communities we serve.
                </p>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default CSR;
