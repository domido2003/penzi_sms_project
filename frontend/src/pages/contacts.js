// src/pages/contacts.js
import React from 'react';
import { Table, Button, Card } from 'react-bootstrap';

const Contacts = () => {
  return (
    <div>
      <h2 className="mb-4">Contacts</h2>

      <Card>
        <Card.Body>
          <Table striped bordered hover>
            <thead>
              <tr>
                <th>Name</th>
                <th>Phone</th>
                <th>Group</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Mary Njeri</td>
                <td>+254 700 123456</td>
                <td>Nairobi Group</td>
              </tr>
              <tr>
                <td>James Otieno</td>
                <td>+254 712 987654</td>
                <td>Birthday Club</td>
              </tr>
              <tr>
                <td>Grace Wambui</td>
                <td>+254 733 456789</td>
                <td>New Leads</td>
              </tr>
            </tbody>
          </Table>
          <Button variant="success">Add New Contact</Button>
        </Card.Body>
      </Card>
    </div>
  );
};

export default Contacts;
