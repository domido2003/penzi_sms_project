import React from 'react';
import Sidebar from '../components/Sidebar';
import Navbar from '../components/Navbar';
import MessageForm from '../components/MessageForm';
import MessageList from '../components/MessageList';
import UserList from '../components/UserList'; //  New import

const Dashboard = () => {
  return (
    <div className="d-flex">
      <Sidebar />
      <div className="flex-grow-1">
        <Navbar />

        <div className="container mt-4">
          <h2>Users</h2>
          <UserList /> {/*  Added user list here */}
        </div>

        <div className="container mt-5">
          <h2>Messages</h2>
          <MessageForm />
          <hr />
          <MessageList />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

