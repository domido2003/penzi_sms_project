import React, { useState, useEffect } from "react";
import axios from "axios";

function MessageForm() {
  const [messageFrom, setMessageFrom] = useState("");
  const [content, setContent] = useState("");
  const [messages, setMessages] = useState([]);
  const [responseMessages, setResponseMessages] = useState([]);

  useEffect(() => {
    fetchMessages();
  }, []);

  const fetchMessages = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/api/messages/");
      setMessages(response.data);
    } catch (error) {
      console.error("❌ Failed to fetch messages:", error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/sms/", {
        message_from: messageFrom,
        message_to: "22141",
        content: content,
        direction: "INCOMING"
      });

      console.log("✅ Message sent:", response.data);
      setMessageFrom("");
      setContent("");
      setResponseMessages(response.data.responses || []);
      fetchMessages(); // Refresh recent messages
    } catch (error) {
      console.error("❌ Error sending message:", error);
      setResponseMessages(["Failed to send message."]);
    }
  };

  return (
    <div
      style={{
        maxWidth: "800px",
        margin: "0 auto",
        padding: "30px",
        background: "#85111115",
        borderRadius: "15px",
        boxShadow: "0 0 15px rgba(22, 8, 10, 0.5)",
        fontFamily: "'Segoe UI', sans-serif",
      }}
    >
      <h2 style={{ color: "#c71585", marginBottom: "20px" }}>💌 Send a Love Message</h2>

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: "15px" }}>
          <label style={{ display: "block", marginBottom: "6px", fontWeight: "bold" }}>
            Your Phone Number
          </label>
          <input
            type="text"
            value={messageFrom}
            onChange={(e) => setMessageFrom(e.target.value)}
            required
            placeholder="07XXXXXXXX"
            style={{
              width: "100%",
              padding: "10px",
              border: "1px solid #0b0203ff",
              borderRadius: "10px",
              outlineColor: "#040bd2ff",
            }}
          />
        </div>

        <div style={{ marginBottom: "15px" }}>
          <label style={{ display: "block", marginBottom: "6px", fontWeight: "bold" }}>
            Message Content
          </label>
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            rows={4}
            required
            placeholder="start#Jane Doe#28#female#Nairobi#Westlands"
            style={{
              width: "100%",
              padding: "10px",
              border: "1px solid #9e056bff",
              borderRadius: "10px",
              outlineColor: "#d6336c",
            }}
          />
        </div>

        <button
          type="submit"
          style={{
            backgroundColor: "#000000ff",
            color: "white",
            padding: "10px 20px",
            border: "none",
            borderRadius: "10px",
            cursor: "pointer",
            fontWeight: "bold",
            fontSize: "16px",
          }}
        >
           👆 Click here to send Message
        </button>
      </form>

      {responseMessages.length > 0 && (
        <div
          style={{
            marginTop: "25px",
            padding: "15px",
            background: "#000000ff",
            border: "1px solid #ffc0cb",
            borderRadius: "12px",
            boxShadow: "0 0 8px rgba(255, 182, 193, 0.3)",
          }}
        >
          <strong style={{ color: "#d6336c" }}>📩 Server Response:</strong>
          <ul style={{ marginTop: "10px" }}>
            {responseMessages.map((msg, idx) => (
              <li key={idx} style={{ padding: "5px 0" }}>
                {msg}
              </li>
            ))}
          </ul>
        </div>
      )}

      <h3 style={{ marginTop: "40px", color: "#c71585" }}>📜 Recent Messages</h3>
      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          marginTop: "15px",
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
              <td style={tableCellStyle}>{new Date(msg.date_created).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// 💖 Shared styles
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

export default MessageForm;

