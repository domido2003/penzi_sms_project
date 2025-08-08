// src/components/Tracking.js

import React, { useEffect, useState } from "react";
import axios from "axios";

function Tracking() {
  const [trackingData, setTrackingData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get("/api/tracking/")
      .then((response) => {
        setTrackingData(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching tracking data:", error);
        setLoading(false);
      });
  }, []);

  return (
    <div>
      <h2 style={{ marginBottom: "20px", color: "#333" }}>
        Match History Tracking
      </h2>

      {loading ? (
        <p>Loading...</p>
      ) : trackingData.length === 0 ? (
        <p>No match tracking data available.</p>
      ) : (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ backgroundColor: "#f8f8f8", color: "#333" }}>
              <th style={cellStyle}>#</th>
              <th style={cellStyle}>Phone Number</th>
              <th style={cellStyle}>Seen Count</th>
              <th style={cellStyle}>Last Updated</th>
            </tr>
          </thead>
          <tbody>
            {trackingData.map((entry, index) => (
              <tr key={entry.id} style={{ backgroundColor: index % 2 === 0 ? "#fff" : "#f2f2f2" }}>
                <td style={cellStyle}>{index + 1}</td>
                <td style={cellStyle}>{entry.phone_number}</td>
                <td style={cellStyle}>{entry.seen_count}</td>
                <td style={cellStyle}>
                  {new Date(entry.last_updated).toLocaleString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

const cellStyle = {
  padding: "10px",
  border: "1px solid #ddd",
  textAlign: "left",
};

export default Tracking;
