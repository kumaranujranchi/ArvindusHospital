import React from 'react';
import { Container, Row, Col, Card } from 'react-bootstrap';

const Blog: React.FC = () => {
  const blogPosts = [
    {
      title: '10 Tips for a Healthy Heart',
      excerpt: 'Learn about simple lifestyle changes that can improve your cardiovascular health.',
      date: '2024-01-15',
      category: 'Cardiology'
    },
    {
      title: 'Understanding Diabetes Management',
      excerpt: 'A comprehensive guide to managing diabetes through diet, exercise, and medication.',
      date: '2024-01-10',
      category: 'General Medicine'
    },
    {
      title: 'The Importance of Regular Health Checkups',
      excerpt: 'Why preventive healthcare is crucial for early detection and treatment of diseases.',
      date: '2024-01-05',
      category: 'Preventive Care'
    }
  ];

  return (
    <div className="page-content">
      <Container>
        <Row>
          <Col lg={12}>
            <div className="page-header">
              <h1>Health Blog</h1>
              <p className="lead">
                Stay informed with the latest health tips and medical insights.
              </p>
            </div>
          </Col>
        </Row>
        
        <Row className="mt-5">
          {blogPosts.map((post, index) => (
            <Col lg={4} md={6} key={index} className="mb-4">
              <Card className="h-100 blog-card">
                <Card.Body>
                  <div className="blog-category mb-2">
                    <span className="badge bg-primary">{post.category}</span>
                  </div>
                  <Card.Title>{post.title}</Card.Title>
                  <Card.Text>{post.excerpt}</Card.Text>
                  <div className="blog-date">
                    <small className="text-muted">{post.date}</small>
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

export default Blog;
