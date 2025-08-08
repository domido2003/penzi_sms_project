import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Messages() {
  const [messages, setMessages] = useState([]);
  //const navigate = useNavigate();

  useEffect(() => {
    fetchMessages();
  }, []);

  const fetchMessages = async () => {
    // const token = localStorage.getItem("accessToken");
    // if (!token) {
    //   navigate("/login");
    //   return;
    // }

    try {
      const response = await axios.get("http://127.0.0.1:8000/api/messages/" /*, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }*/);
      setMessages(response.data);
    } catch (error) {
      console.error("❌ Failed to fetch messages:", error);
      // if (error.response && error.response.status === 401) {
      //   navigate("/login");
      // }
    }
  };

  return (
    <div style={{ padding: "30px" }}>
      <h2 style={{ color: "#c71585", marginBottom: "20px" }}>📜 All Messages</h2>

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          background: "#fff",
          borderRadius: "10px",
          overflow: "hidden",
          boxShadow: "0 0 10px rgba(221, 160, 221, 0.2)",
        }}
      >
        <thead style={{ backgroundColor: "#15050bff" }}>
          <tr>
            <th style={tableHeaderStyle}>From</th>
            <th style={tableHeaderStyle}>To</th>
            <th style={tableHeaderStyle}>Content</th>
            <th style={tableHeaderStyle}>Direction</th>
            <th style={tableHeaderStyle}>Date</th>
          </tr>
        </thead>
        <tbody>
          {messages.map((msg, index) => (
            <tr key={index}>
              <td style={tableCellStyle}>{msg.message_from}</td>
              <td style={tableCellStyle}>{msg.message_to}</td>
              <td style={tableCellStyle}>{msg.content}</td>
              <td style={tableCellStyle}>{msg.direction}</td>
              <td style={tableCellStyle}>
                {new Date(msg.date_created).toLocaleString()}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const tableHeaderStyle = {
  padding: "10px",
  borderBottom: "2px solid #ffc0cb",
  fontWeight: "bold",
  color: "#c71585",
  textAlign: "left",
};

const tableCellStyle = {
  padding: "10px",
  borderBottom: "1px solid #000000ff",
};

export default Messages;
