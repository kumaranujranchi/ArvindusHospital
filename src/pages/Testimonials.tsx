import React from 'react';
import { Container, Row, Col, Card } from 'react-bootstrap';

const Testimonials: React.FC = () => {
  const testimonials = [
    {
      name: 'Rajesh Kumar',
      location: 'Patna',
      message: 'Excellent care and professional staff. The doctors are very knowledgeable and caring.',
      rating: 5
    },
    {
      name: 'Priya Sharma',
      location: 'Chapra',
      message: 'Great hospital with modern facilities. I received the best treatment here.',
      rating: 5
    },
    {
      name: 'Amit Singh',
      location: 'Jamui',
      message: 'Highly recommend Arvindu Hospitals. The staff is very supportive and caring.',
      rating: 5
    }
  ];

  return (
    <div className="page-content">
      <Container>
        <Row>
          <Col lg={12}>
            <div className="page-header">
              <h1>Patient Testimonials</h1>
              <p className="lead">
                Hear what our patients have to say about their experience with us.
              </p>
            </div>
          </Col>
        </Row>
        
        <Row className="mt-5">
          {testimonials.map((testimonial, index) => (
            <Col lg={4} md={6} key={index} className="mb-4">
              <Card className="h-100 testimonial-card">
                <Card.Body>
                  <div className="rating mb-3">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <i key={i} className="fas fa-star text-warning"></i>
                    ))}
                  </div>
                  <Card.Text>"{testimonial.message}"</Card.Text>
                  <div className="testimonial-author">
                    <strong>{testimonial.name}</strong>
                    <br />
                    <small className="text-muted">{testimonial.location}</small>
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

export default Testimonials;
