import React from 'react';
import { Navbar, Nav, NavDropdown, Container } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';
import { useLocation } from 'react-router-dom';

const Header: React.FC = () => {
  const location = useLocation();

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <header>
      <Navbar expand="lg" className="navbar-light">
        <Container>
          <LinkContainer to="/">
            <Navbar.Brand>
              <img 
                src="/images/logo.svg" 
                alt="Arvindu Hospitals Logo"
                style={{ height: '40px' }}
              />
            </Navbar.Brand>
          </LinkContainer>
          
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="ms-auto">
              <LinkContainer to="/">
                <Nav.Link className={isActive('/') || isActive('/home') ? 'active' : ''}>
                  Home
                </Nav.Link>
              </LinkContainer>
              
              <LinkContainer to="/about">
                <Nav.Link className={isActive('/about') ? 'active' : ''}>
                  About Us
                </Nav.Link>
              </LinkContainer>
              
              <LinkContainer to="/departments">
                <Nav.Link className={isActive('/departments') ? 'active' : ''}>
                  Departments & Specialties
                </Nav.Link>
              </LinkContainer>
              
              <LinkContainer to="/doctors">
                <Nav.Link className={isActive('/doctors') ? 'active' : ''}>
                  Find a Doctor
                </Nav.Link>
              </LinkContainer>
              
              <LinkContainer to="/patient-care">
                <Nav.Link className={isActive('/patient-care') ? 'active' : ''}>
                  Patient Care
                </Nav.Link>
              </LinkContainer>
              
              <NavDropdown title="More" id="basic-nav-dropdown">
                <LinkContainer to="/testimonials">
                  <NavDropdown.Item className={isActive('/testimonials') ? 'active' : ''}>
                    Testimonials
                  </NavDropdown.Item>
                </LinkContainer>
                
                <LinkContainer to="/blog">
                  <NavDropdown.Item className={isActive('/blog') ? 'active' : ''}>
                    Health Blog
                  </NavDropdown.Item>
                </LinkContainer>
                
                <LinkContainer to="/careers">
                  <NavDropdown.Item className={isActive('/careers') ? 'active' : ''}>
                    Career Opportunities
                  </NavDropdown.Item>
                </LinkContainer>
                
                <LinkContainer to="/news">
                  <NavDropdown.Item className={isActive('/news') ? 'active' : ''}>
                    Media & News
                  </NavDropdown.Item>
                </LinkContainer>
                
                <LinkContainer to="/csr">
                  <NavDropdown.Item className={isActive('/csr') ? 'active' : ''}>
                    CSR Initiatives
                  </NavDropdown.Item>
                </LinkContainer>
                
                <LinkContainer to="/contact">
                  <NavDropdown.Item className={isActive('/contact') ? 'active' : ''}>
                    Contact Us
                  </NavDropdown.Item>
                </LinkContainer>
              </NavDropdown>
              
              <LinkContainer to="/appointment">
                <Nav.Link className={`nav-appointment-btn ${isActive('/appointment') ? 'active' : ''}`}>
                  Book Appointment
                </Nav.Link>
              </LinkContainer>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </header>
  );
};

export default Header;
