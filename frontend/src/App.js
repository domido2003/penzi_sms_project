// src/App.js
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import MessageForm from './components/MessageForm';
import MessageList from './components/MessageList';
import Users from './components/Users';
import Tracking from './components/Tracking';
import SendSmsForm from './components/SendSmsForm';

function App() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      {/* 💖 Themed Header with Local Logo */}
      <header style={{
        display: 'flex',
        alignItems: 'center',
        padding: '16px 24px',
        backgroundColor: '#a04363ff',
        color: 'white',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
      }}>
        <img
        src='onfon.jpeg'
          alt="Onfon Media Logo"
          style={{ height: '48px', marginRight: '16px' }}
        />
        <h1 style={{
          fontSize: '1.8rem',
          fontFamily: "'Playfair Display', serif",
          margin: 0
        }}>
          PENZI  DASHBOARD
        </h1>
      </header>

      <div style={{ display: 'flex', flex: 1 }}>
        <Sidebar />
        <div style={{
          flex: 1,
          padding: '20px',
          backgroundColor: '#2a1019ff'
        }}>
          <Routes>
            <Route path="/" element={<Navigate to="/messages" replace />} />
            <Route path="/messages" element={<><MessageForm /><MessageList /></>} />
            <Route path="/users" element={<Users />} />
            <Route path="/tracking" element={<Tracking />} />
            <Route path="/simulate" element={<SendSmsForm />} />
          </Routes>
        </div>
      </div>
    </div>
  );
}

export default App;
