import React, { useEffect, useState } from 'react';
import axios from 'axios';

const UserList = () => {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    // Fetch users from your Django backend
    axios.get('http://127.0.0.1:8000/api/users/')
      .then(response => {
        setUsers(response.data);
      })
      .catch(error => {
        console.error('Error fetching users:', error);
      });
  }, []);

  return (
    <div className="table-responsive">
      <table className="table table-bordered table-striped">
        <thead className="thead-dark">
          <tr>
            <th>Full Name</th>
            <th>Phone</th>
            <th>Age</th>
            <th>Gender</th>
            <th>County</th>
            <th>Town</th>
            <th>Education</th>
            <th>Profession</th>
            <th>Marital</th>
            <th>Religion</th>
            <th>Ethnicity</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          {users.length > 0 ? (
            users.map(user => (
              <tr key={user.id}>
                <td>{user.full_name}</td>
                <td>{user.phone_number}</td>
                <td>{user.age}</td>
                <td>{user.gender}</td>
                <td>{user.county}</td>
                <td>{user.town}</td>
                <td>{user.education_level || '-'}</td>
                <td>{user.profession || '-'}</td>
                <td>{user.marital_status || '-'}</td>
                <td>{user.religion || '-'}</td>
                <td>{user.ethnicity || '-'}</td>
                <td>{user.self_description || '-'}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="12" className="text-center">No users found</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default UserList;
