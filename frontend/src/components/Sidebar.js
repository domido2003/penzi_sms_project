// src/components/Sidebar.js
import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Sidebar = () => {
  const location = useLocation();
  const navItems = [
    { label: '📨 Messages', path: '/messages' },
    { label: '👤 Users', path: '/users' },
    { label: '📍 Tracking', path: '/tracking' },
    { label: '💬 Simulate SMS', path: '/simulate' }
  ];

  const logo = process.env.PUBLIC_URL + '/onfon.jpeg';

  return (
    <div style={{
      width: '250px',
      height: '100vh',
      backgroundColor: '#121212',
      padding: '24px 20px',
      boxShadow: '2px 0 6px rgba(0,0,0,0.3)',
      color: '#fff',
      display: 'flex',
      flexDirection: 'column',
    }}>
      
      {/* 🔷 Plain Zoomed Logo & Welcome Text */}
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        marginBottom: '35px'
      }}>
        <img
          src={logo}
          alt="Onfon Logo"
          style={{
            width: '60px',
            height: '60px',
            objectFit: 'cover', // zoom in
            // Removed border radius & shadow
          }}
        />
        <p style={{
          marginTop: '10px',
          fontSize: '1rem',
          fontWeight: 'bold',
          letterSpacing: '1px',
          color: '#ff99aa'
        }}>
          WELCOME ADMIN
        </p>
      </div>

      {/* 🔷 Navigation */}
      <ul style={{ listStyle: 'none', padding: 0, marginTop: '10px' }}>
        {navItems.map((item, index) => (
          <li key={index} style={{ marginBottom: '12px' }}>
            <Link
              to={item.path}
              style={{
                textDecoration: 'none',
                color: location.pathname === item.path ? '#fff' : '#ccc',
                backgroundColor: location.pathname === item.path ? '#ff4d6d' : 'transparent',
                padding: '12px 18px',
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
