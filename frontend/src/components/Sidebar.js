// src/components/Sidebar.js

import React from "react";
import { Link, useLocation } from "react-router-dom";

function Sidebar() {
  const location = useLocation();

  const navItems = [
    { name: "MESSAGES", path: "/messages" },
    { name: "USERS", path: "/users" },
    { name: "TRACKING", path: "/tracking" },
    { name: "SIMULATE SMS", path: "/simulate" },
    { name: "LOGISTICS", path: "/logistics" }, // ✅ New item
  ];

  return (
    <div
      style={{
        width: "260px",
        backgroundColor: "#2c2c2c",
        color: "#fff",
        height: "100vh",
        padding: "20px",
        display: "flex",
        flexDirection: "column",
        gap: "20px",
        boxShadow: "2px 0 5px rgba(0, 0, 0, 0.2)",
      }}
    >
      {/* Moving Heading */}
      <div style={{ overflow: "hidden", height: "50px", marginBottom: "40px" }}>
        <div
          style={{
            whiteSpace: "nowrap",
            display: "inline-block",
            animation: "slide-left 20s linear infinite",
            fontWeight: "900",
            fontSize: "22px",
            color: "#4da6ff",
            textTransform: "uppercase",
            letterSpacing: "0.5px",
          }}
        >
          Welcome to the Onfon Penzi SMS dating dashboard. What do you want to access today?
        </div>
      </div>

      {/* Navigation */}
      {navItems.map((item) => (
        <Link
          key={item.path}
          to={item.path}
          style={{
            color: location.pathname === item.path ? "#ff99aa" : "#fff",
            textDecoration: "none",
            padding: "10px 15px",
            borderRadius: "6px",
            backgroundColor:
              location.pathname === item.path ? "#444" : "transparent",
            fontWeight: "500",
            transition: "all 0.2s ease",
          }}
        >
          {item.name}
        </Link>
      ))}

      {/* Keyframes */}
      <style>
        {`
          @keyframes slide-left {
            0% {
              transform: translateX(100%);
            }
            100% {
              transform: translateX(-100%);
            }
          }
        `}
      </style>
    </div>
  );
}

export default Sidebar;
