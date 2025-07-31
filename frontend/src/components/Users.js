import React, { useEffect, useState } from 'react';
import axios from 'axios';

const thStyle = {
  borderBottom: "2px solid #ccc",
  padding: "10px",
  background: "#ffe6e6",
  textAlign: "left",
};

const tdStyle = {
  padding: "10px",
  borderBottom: "1px solid #ddd",
};

const buttonStyle = {
  padding: "8px 15px",
  margin: "0 5px",
  backgroundColor: "#b30000",
  color: "white",
  border: "none",
  borderRadius: "5px",
  cursor: "pointer",
};

const cardStyle = {
  border: "1px solid #ccc",
  padding: "15px",
  borderRadius: "10px",
  marginBottom: "15px",
  backgroundColor: "#fff",
  boxShadow: "0 0 5px rgba(0,0,0,0.1)",
};

const inputStyle = {
  padding: "8px",
  width: "100%",
  maxWidth: "400px",
  marginBottom: "20px",
  borderRadius: "5px",
  border: "1px solid #ccc",
};

const Users = () => {
  const [users, setUsers] = useState([]);
  const [filteredUsers, setFilteredUsers] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [totalUsers, setTotalUsers] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    fetchUsers(currentPage);
  }, [currentPage]);

  const fetchUsers = async (page) => {
    try {
      const res = await axios.get(`http://127.0.0.1:8000/api/users/?page=${page}`);
      setUsers(res.data.users);
      setFilteredUsers(res.data.users);
      setTotalUsers(res.data.total_users);
      setTotalPages(res.data.total_pages);
    } catch (error) {
      console.error("❌ Failed to fetch users:", error);
    }
  };

  useEffect(() => {
    const lowerSearch = searchTerm.toLowerCase();
    const filtered = users.filter(user =>
      Object.values(user).some(value =>
        String(value).toLowerCase().includes(lowerSearch)
      )
    );
    setFilteredUsers(filtered);
  }, [searchTerm, users]);

  const handleNext = () => {
    if (currentPage < totalPages) setCurrentPage(prev => prev + 1);
  };

  const handlePrevious = () => {
    if (currentPage > 1) setCurrentPage(prev => prev - 1);
  };

  return (
    <div style={{ padding: "20px", background: "#fdf0f0", minHeight: "100vh" }}>
      <h2 style={{ marginBottom: "10px", color: "#8B0000" }}>📋 Registered Users</h2>
      <p>Total Users: <strong>{totalUsers}</strong></p>

      <input
        type="text"
        placeholder="🔍 Search users..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        style={inputStyle}
      />

      {filteredUsers.length === 0 ? (
        <p>No users found.</p>
      ) : (
        <>
          {/* Desktop Table (shows on wide screens) */}
          <div className="user-table" style={{ overflowX: "auto", marginBottom: "20px" }}>
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr>
                  <th style={thStyle}>Full Name</th>
                  <th style={thStyle}>Phone</th>
                  <th style={thStyle}>Age</th>
                  <th style={thStyle}>Gender</th>
                  <th style={thStyle}>County</th>
                  <th style={thStyle}>Town</th>
                  <th style={thStyle}>Education</th>
                  <th style={thStyle}>Profession</th>
                  <th style={thStyle}>Marital</th>
                  <th style={thStyle}>Religion</th>
                  <th style={thStyle}>Ethnicity</th>
                  <th style={thStyle}>Description</th>
                  <th style={thStyle}>Date Joined</th>
                </tr>
              </thead>
              <tbody>
                {filteredUsers.map((user, index) => (
                  <tr key={index}>
                    <td style={tdStyle}>{user.full_name}</td>
                    <td style={tdStyle}>{user.phone_number}</td>
                    <td style={tdStyle}>{user.age}</td>
                    <td style={tdStyle}>{user.gender}</td>
                    <td style={tdStyle}>{user.county}</td>
                    <td style={tdStyle}>{user.town}</td>
                    <td style={tdStyle}>{user.education_level}</td>
                    <td style={tdStyle}>{user.profession}</td>
                    <td style={tdStyle}>{user.marital_status}</td>
                    <td style={tdStyle}>{user.religion}</td>
                    <td style={tdStyle}>{user.ethnicity}</td>
                    <td style={tdStyle}>{user.self_description}</td>
                    <td style={tdStyle}>
                      {new Date(user.date_created).toLocaleDateString("en-GB", {
                        day: "2-digit",
                        month: "short",
                        year: "numeric",
                      })}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Mobile Card view (optional) */}
          <div className="card-container" style={{ display: "none" }}>
            {filteredUsers.map((user, index) => (
              <div key={index} style={cardStyle}>
                <p><strong>Name:</strong> {user.full_name}</p>
                <p><strong>Phone:</strong> {user.phone_number}</p>
                <p><strong>Age:</strong> {user.age}</p>
                <p><strong>Gender:</strong> {user.gender}</p>
                <p><strong>County:</strong> {user.county}</p>
                <p><strong>Town:</strong> {user.town}</p>
                <p><strong>Education:</strong> {user.education_level}</p>
                <p><strong>Profession:</strong> {user.profession}</p>
                <p><strong>Marital:</strong> {user.marital_status}</p>
                <p><strong>Religion:</strong> {user.religion}</p>
                <p><strong>Ethnicity:</strong> {user.ethnicity}</p>
                <p><strong>Description:</strong> {user.self_description}</p>
                <p><strong>Date Joined:</strong> {new Date(user.date_created).toLocaleDateString("en-GB", {
                  day: "2-digit",
                  month: "short",
                  year: "numeric",
                })}</p>
              </div>
            ))}
          </div>
        </>
      )}

      {/* Pagination */}
      <div style={{ marginTop: "20px" }}>
        <button onClick={handlePrevious} disabled={currentPage === 1} style={buttonStyle}>⬅ Prev</button>
        <span style={{ margin: "0 15px" }}>Page {currentPage} of {totalPages}</span>
        <button onClick={handleNext} disabled={currentPage === totalPages} style={buttonStyle}>Next ➡</button>
      </div>
    </div>
  );
};

export default Users;
