import React, { useEffect, useState } from "react";
import axios from "axios";

function Users() {
  const [users, setUsers] = useState([]);
  const [totalCount, setTotalCount] = useState(0);
  const [page, setPage] = useState(1);
  const [pageSize] = useState(30);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await axios.get(
          `http://localhost:8000/api/users/?page=${page}&search=${encodeURIComponent(searchTerm)}`
        );

        const data = response.data;

        if (Array.isArray(data)) {
          setUsers(data);
          setTotalCount(data.length);
        } else {
          setUsers(data.results || []);
          setTotalCount(data.count || 0);
        }
      } catch (error) {
        console.error("❌ Failed to fetch users:", error);
        // No redirect, just show error in console for now
      }
    };

    fetchUsers();
  }, [page, searchTerm]);

  const totalPages = Math.max(1, Math.ceil(totalCount / pageSize));

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2>Registered Users</h2>
        <input
          type="text"
          className="form-control w-25"
          placeholder="Search by name or phone"
          value={searchTerm}
          onChange={(e) => {
            setSearchTerm(e.target.value);
            setPage(1);
          }}
          onKeyPress={(e) => {
            if (e.key === "Enter") {
              // No manual fetch needed; useEffect triggers fetch on searchTerm change
            }
          }}
        />
      </div>

      <p>Total Users: <strong>{totalCount}</strong></p>

      <div className="table-responsive">
        <table className="table table-striped table-bordered table-sm">
          <thead className="table-dark">
            <tr>
              <th>ID</th>
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
              <th>Joined</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.id}>
                <td>{user.id}</td>
                <td>{user.full_name}</td>
                <td>{user.phone_number}</td>
                <td>{user.age}</td>
                <td>{user.gender}</td>
                <td>{user.county}</td>
                <td>{user.town}</td>
                <td>{user.education_level}</td>
                <td>{user.profession}</td>
                <td>{user.marital_status}</td>
                <td>{user.religion}</td>
                <td>{user.ethnicity}</td>
                <td>{new Date(user.date_created).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="d-flex justify-content-between mt-3">
        <button
          className="btn btn-secondary"
          onClick={() => setPage((prev) => Math.max(prev - 1, 1))}
          disabled={page === 1}
        >
          Previous
        </button>
        <span>Page {page} of {totalPages}</span>
        <button
          className="btn btn-secondary"
          onClick={() => setPage((prev) => Math.min(prev + 1, totalPages))}
          disabled={page === totalPages}
        >
          Next
        </button>
      </div>
    </div>
  );
}

export default Users;
