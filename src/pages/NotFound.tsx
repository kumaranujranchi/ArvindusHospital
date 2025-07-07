import React from 'react';
import { Container, Row, Col, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const NotFound: React.FC = () => {
  return (
    <div className="page-content">
      <Container>
        <Row>
          <Col lg={12} className="text-center">
            <div className="error-page">
              <h1 className="display-1 text-primary">404</h1>
              <h2 className="mb-4">Page Not Found</h2>
              <p className="lead mb-4">
                Sorry, the page you are looking for doesn't exist or has been moved.
              </p>
              <Link to="/">
                <Button variant="primary" size="lg">
                  Go to Home
                </Button>
              </Link>
            </div>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default NotFound;
