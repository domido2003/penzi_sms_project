import React, { useState } from 'react';
import axios from 'axios';

const Messages = () => {
  const [message, setMessage] = useState('');
  const [recipient, setRecipient] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://127.0.0.1:8000/api/messages/', {
        message_to: recipient,
        content: message,
        direction: 'outgoing',  // assuming this is for outgoing messages
      });
      alert("Message sent!");
      setMessage('');
      setRecipient('');
    } catch (err) {
      console.error(err);
      alert("Failed to send message.");
    }
  };

  return (
    <div className="container mt-4">
      <h3>Send a Message</h3>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label>Recipient Phone Number</label>
          <input
            type="text"
            className="form-control"
            value={recipient}
            onChange={(e) => setRecipient(e.target.value)}
            required
          />
        </div>
        <div className="mb-3">
          <label>Message</label>
          <textarea
            className="form-control"
            rows="3"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            required
          ></textarea>
        </div>
        <button type="submit" className="btn btn-primary">Send</button>
      </form>
    </div>
  );
};

export default Messages;
