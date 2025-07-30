import React, { useEffect, useState } from 'react';
import axios from 'axios';

const MessageList = () => {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    fetchMessages();
  }, []);

  const fetchMessages = async () => {
    try {
      const res = await axios.get('http://127.0.0.1:8000/api/messages/');
      setMessages(res.data);
    } catch (error) {
      console.error('Failed to fetch messages:', error);
    }
  };

  return (
    <div>
      <h5>Recent Messages</h5>
      <table className="table table-bordered">
        <thead>
          <tr>
            <th>From</th>
            <th>To</th>
            <th>Content</th>
            <th>Direction</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {messages.map((msg, index) => (
            <tr key={index}>
              <td>{msg.message_from}</td>
              <td>{msg.message_to}</td>
              <td>{msg.content}</td>
              <td>{msg.direction}</td>
              <td>{msg.date_created}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default MessageList;
