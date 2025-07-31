// src/components/MessageForm.js

import React, { useState, useEffect } from "react";
import axios from "axios";

function MessageForm() {
  const [messageFrom, setMessageFrom] = useState("");
  const [content, setContent] = useState("");
  const [messages, setMessages] = useState([]);
  const [serverResponse, setServerResponse] = useState("");

  useEffect(() => {
    fetchMessages();
  }, []);

  const fetchMessages = async () => {
    try {
      const res = await axios.get("http://localhost:8000/api/messages/");
      setMessages(res.data);
    } catch (error) {
      console.error("Failed to fetch messages", error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://localhost:8000/api/sms/", {
        message_from: messageFrom,
        content,
      });

      console.log("📥 Backend response:", res.data); // Debug log
      setServerResponse(res.data.response); // <-- Ensure this matches Django key
      setContent("");
      fetchMessages();
    } catch (error) {
      console.error("❌ Failed to send SMS:", error.response?.data || error.message);
      setServerResponse("❌ Failed: " + (error.response?.data?.error || error.message));
    }
  };

  const getDynamicHint = () => {
    const lower = content.toLowerCase();
    if (lower.startsWith("start#")) {
      return "Format: start#Jane Doe#25#Female#Nairobi#Westlands";
    } else if (lower.startsWith("details#")) {
      return "Format: details#Graduate#Teacher#Single#Christian#Kamba";
    } else if (lower.startsWith("myself#")) {
      return "Format: myself#I am adventurous and kind.";
    } else if (lower.startsWith("match#")) {
      return "Format: match#25-30#Nairobi";
    } else if (lower.startsWith("describe#")) {
      return "Format: describe#07XXXXXXXX";
    } else if (lower === "yes" || lower === "yes#") {
      return "Reply YES to accept the interest and receive full profile.";
    } else if (/^07\d{8}$/.test(lower)) {
      return "Enter a number to request that profile.";
    } else {
      return "e.g. start#Jane Doe#25#Female#Nairobi#Westlands";
    }
  };

  return (
    <div style={{ padding: "20px", background: "#fff5f5", minHeight: "100vh" }}>
      <h2 style={{ color: "#b30000", marginBottom: "20px" }}>📨 Send SMS Command</h2>

      <form onSubmit={handleSubmit} style={{ display: "flex", gap: "10px", flexWrap: "wrap", marginBottom: "10px" }}>
        <input
          type="text"
          placeholder="Sender's phone number"
          value={messageFrom}
          onChange={(e) => setMessageFrom(e.target.value)}
          required
          style={{
            flex: "1 1 200px",
            padding: "10px",
            borderRadius: "5px",
            border: "1px solid #ccc",
          }}
        />
        <input
          type="text"
          placeholder={getDynamicHint()}
          value={content}
          onChange={(e) => setContent(e.target.value)}
          required
          style={{
            flex: "2 1 400px",
            padding: "10px",
            borderRadius: "5px",
            border: "1px solid #ccc",
          }}
        />
        <button
          type="submit"
          style={{
            backgroundColor: "#e63946",
            color: "#fff",
            border: "none",
            borderRadius: "5px",
            padding: "10px 20px",
            cursor: "pointer",
          }}
        >
          Send
        </button>
      </form>

      {/* Dynamic Format Hint */}
      <div
        style={{
          background: "#ffe6e6",
          border: "1px solid #ffcccc",
          borderRadius: "6px",
          padding: "10px",
          fontSize: "13px",
          marginBottom: "15px",
          color: "#5a0000",
        }}
      >
        <strong>Format Hint:</strong> {getDynamicHint()}
      </div>

      {/* Server Response Box */}
      {serverResponse && (
        <div
          style={{
            backgroundColor: "#e6f4ea",
            color: "#0b5134",
            border: "1px solid #b4dfc5",
            borderRadius: "6px",
            padding: "12px",
            marginBottom: "25px",
            whiteSpace: "pre-wrap",
            lineHeight: "1.6",
          }}
        >
          <strong>📩 Server Response:</strong><br />
          {serverResponse}
        </div>
      )}

      {/* Message Table */}
      <div style={{ overflowX: "auto" }}>
        <h3 style={{ marginBottom: "10px", color: "#8B0000" }}>📋 Message Log</h3>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ backgroundColor: "#ffcccc" }}>
              <th style={tableHeaderStyle}>Direction</th>
              <th style={tableHeaderStyle}>From</th>
              <th style={tableHeaderStyle}>To</th>
              <th style={tableHeaderStyle}>Content</th>
              <th style={tableHeaderStyle}>Date</th>
            </tr>
          </thead>
          <tbody>
            {messages.map((msg) => (
              <tr key={msg.id}>
                <td style={tableCellStyle}>{msg.direction}</td>
                <td style={tableCellStyle}>{msg.message_from}</td>
                <td style={tableCellStyle}>{msg.message_to}</td>
                <td style={tableCellStyle}>{msg.content}</td>
                <td style={tableCellStyle}>
                  {new Date(msg.date_created).toLocaleString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// Table styling
const tableHeaderStyle = {
  padding: "10px",
  borderBottom: "2px solid #ccc",
  textAlign: "left",
  color: "#b30000",
};

const tableCellStyle = {
  padding: "10px",
  borderBottom: "1px solid #eee",
};

export default MessageForm;
