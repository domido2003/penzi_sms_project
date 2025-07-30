// src/components/Sidebar.js
import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Sidebar = () => {
  const location = useLocation();

  const navItems = [
    { label: ' MESSAGES', path: '/messages' },
    { label: '👤 Users', path: '/users' },
    { label: ' TRACKING', path: '/tracking' },
    { label: ' SIMULATE SMS', path: '/simulate' }
  ];

  return (
    <div style={{
      width: '220px',
      height: '100vh',
      backgroundColor: '#121212', // Elegant black
      padding: '20px',
      boxShadow: '2px 0 6px rgba(0,0,0,0.3)',
      color: '#fff'
    }}>
      <h2 style={{ color: '#ff99aa', marginBottom: '24px' }}>☕ Dashboard</h2>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {navItems.map((item, index) => (
          <li key={index} style={{ marginBottom: '12px' }}>
            <Link
              to={item.path}
              style={{
                textDecoration: 'none',
                color: location.pathname === item.path ? '#fff' : '#ccc',
                backgroundColor: location.pathname === item.path ? '#ff4d6d' : 'transparent',
                padding: '10px 16px',
                display: 'block',
                borderRadius: '8px',
                fontWeight: '500',
                transition: 'all 0.3s ease'
              }}
            >
              {item.label}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Sidebar;
