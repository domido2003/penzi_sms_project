import React from 'react';
import Sidebar from './Sidebar';
import { Container, Row, Col } from 'react-bootstrap';

const Layout = ({ children }) => {
  return (
    <Container fluid>
      <Row>
        <Col md={2} className="bg-dark text-white min-vh-100">
          <Sidebar />
        </Col>
        <Col md={10} className="p-4">
          {children}
        </Col>
      </Row>
    </Container>
  );
};

export default Layout;
