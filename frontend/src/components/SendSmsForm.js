import React, { useState } from "react";

function SendSmsForm() {
  const [messageTo, setMessageTo] = useState("22141");
  const [content, setContent] = useState("");
  const [response, setResponse] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    const payload = {
      message_to: messageTo,
      content: content,
      direction: "INCOMING"
    };

    try {
      const res = await fetch("http://127.0.0.1:8000/api/sms/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      const data = await res.json();
      setResponse(data.message || "Message sent.");
    } catch (err) {
      console.error(err);
      setResponse("❌ Error sending message.");
    }
  };

  return (
    <div>
      <h3>📩 Send Simulated SMS</h3>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={messageTo}
          onChange={(e) => setMessageTo(e.target.value)}
          placeholder="Message To (e.g. 22141)"
          required
        /><br /><br />
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="SMS content (e.g. start#John Doe#24#Male#Nairobi#Thika)"
          rows={4}
          required
        /><br /><br />
        <button type="submit">Send Message</button>
      </form>
      {response && <p>✅ {response}</p>}
    </div>
  );
}

export default SendSmsForm;
