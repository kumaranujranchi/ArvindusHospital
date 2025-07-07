import React from 'react';
import { Container, Row, Col, Card } from 'react-bootstrap';

const News: React.FC = () => {
  const newsItems = [
    {
      title: 'Arvindu Hospitals Opens New Jamui Branch',
      excerpt: 'We are excited to announce the opening of our new facility in Jamui, bringing quality healthcare closer to the community.',
      date: '2024-01-20',
      category: 'Hospital News'
    },
    {
      title: 'New Cardiac Care Unit Launched',
      excerpt: 'State-of-the-art cardiac care unit with advanced equipment now operational at our Patna branch.',
      date: '2024-01-15',
      category: 'Medical Updates'
    },
    {
      title: 'Free Health Camp in Rural Areas',
      excerpt: 'Arvindu Hospitals conducts free health screening camps in rural areas of Bihar.',
      date: '2024-01-10',
      category: 'Community Service'
    }
  ];

  return (
    <div className="page-content">
      <Container>
        <Row>
          <Col lg={12}>
            <div className="page-header">
              <h1>Media & News</h1>
              <p className="lead">
                Stay updated with the latest news and announcements from Arvindu Hospitals.
              </p>
            </div>
          </Col>
        </Row>
        
        <Row className="mt-5">
          {newsItems.map((news, index) => (
            <Col lg={4} md={6} key={index} className="mb-4">
              <Card className="h-100 news-card">
                <Card.Body>
                  <div className="news-category mb-2">
                    <span className="badge bg-success">{news.category}</span>
                  </div>
                  <Card.Title>{news.title}</Card.Title>
                  <Card.Text>{news.excerpt}</Card.Text>
                  <div className="news-date">
                    <small className="text-muted">{news.date}</small>
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

export default News;
