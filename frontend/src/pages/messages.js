import React, { useState, useEffect } from "react";
import axios from "axios";

export default function Messages() {
  const [messages, setMessages] = useState([]);
  const [showWelcome, setShowWelcome] = useState(false);

  useEffect(() => {
    fetchMessages();
  }, []);

  const fetchMessages = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/api/messages/");
      const sortedMessages = response.data.sort(
        (a, b) => new Date(a.date_created) - new Date(b.date_created) // oldest → newest
      );
      setMessages(sortedMessages);

      if (response.data.length === 0) {
        setShowWelcome(true);
      } else {
        setShowWelcome(false);
      }
    } catch (error) {
      console.error("❌ Failed to fetch messages:", error);
      setShowWelcome(true);
    }
  };

  // Same guidance logic from MessageForm
  const getNextStepGuide = (messageText) => {
    const text = messageText.toLowerCase();
    if (text.startsWith("start#")) {
      return "✅ Profile created. Next: SMS details#levelOfEducation#profession#maritalStatus#religion#ethnicity to 22141.\nExample: details#diploma#driver#single#christian#mijikenda";
    }
    if (text.startsWith("details#")) {
      return "✅ Details saved. Next: SMS a brief description starting with MYSELF.\nExample: MYSELF chocolate, lovely, sexy etc.";
    }
    if (text.startsWith("myself")) {
      return "✅ Description saved. You can now search for a MPENZI.\nExample: match#23-25#Nairobi";
    }
    if (text.startsWith("match#")) {
      return "🔍 Searching for matches… You will receive details shortly.";
    }
    if (text === "next") {
      return "➡ Showing next set of matches.";
    }
    if (/^\d{10}$/.test(text)) {
      return "📩 Requesting more details for this person.";
    }
    if (text.startsWith("describe")) {
      return "ℹ Showing self-description of the person.";
    }
    if (text === "yes") {
      return "✅ Confirmation sent. You will receive full details shortly.";
    }
    return "";
  };

  return (
    <div style={{ padding: "20px", maxWidth: "800px", margin: "auto" }}>
      <h2 style={{ color: "#c71585", marginBottom: "20px" }}>📜 All Messages</h2>

      {showWelcome && (
        <div
          style={{
            marginBottom: "20px",
            padding: "15px",
            backgroundColor: "#fff3cd",
            border: "1px solid #ffeeba",
            borderRadius: "10px",
            color: "#856404",
            whiteSpace: "pre-line",
          }}
        >
          PENZI User Onfon{"\n"}
          Welcome to our dating service with 6000 potential dating partners!{"\n"}
          To register SMS start#name#age#gender#county#town to 22141.{"\n"}
          E.g., start#John Doe#26#Male#Nakuru#Naivasha
        </div>
      )}

      <div
        style={{
          maxHeight: "500px",
          overflowY: "auto",
          backgroundColor: "#f8f9fa",
          padding: "15px",
          borderRadius: "10px",
          boxShadow: "0 0 10px rgba(0,0,0,0.1)",
        }}
      >
        {messages.length === 0 && !showWelcome ? (
          <p style={{ textAlign: "center", color: "#777" }}>No messages found.</p>
        ) : (
          messages.map((msg, index) => {
            const isOutgoing =
              msg.direction && msg.direction.toUpperCase() === "OUTGOING";
            const guide = getNextStepGuide(msg.content);
            return (
              <div
                key={index}
                style={{
                  display: "flex",
                  justifyContent: isOutgoing ? "flex-end" : "flex-start",
                  marginBottom: "12px",
                }}
              >
                <div
                  style={{
                    backgroundColor: isOutgoing ? "#d4edda" : "#cce5ff",
                    color: isOutgoing ? "#155724" : "#004085",
                    padding: "10px 14px",
                    borderRadius: "12px",
                    maxWidth: "70%",
                    boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
                    wordBreak: "break-word",
                  }}
                >
                  <div style={{ fontSize: "0.85em", marginBottom: "4px" }}>
                    {isOutgoing
                      ? `📤 To: ${msg.message_to || "N/A"}`
                      : `📥 From: ${msg.message_from || "N/A"}`}
                  </div>
                  <div>{msg.content}</div>
                  <div
                    style={{
                      fontSize: "0.75em",
                      color: "#555",
                      marginTop: "5px",
                      whiteSpace: "pre-line",
                    }}
                  >
                    {new Date(msg.date_created).toLocaleString()}
                    {guide && (
                      <div
                        style={{
                          marginTop: "6px",
                          padding: "6px",
                          background: isOutgoing ? "#fdfd96" : "#fff3cd",
                          borderRadius: "6px",
                          fontSize: "0.8em",
                          color: "#856404",
                        }}
                      >
                        {guide}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
