import React from "react";
import Sidebar from "./Sidebar";
import { Outlet } from "react-router-dom";

const Layout = () => {
  return (
    <div style={{ display: "flex", height: "100vh", overflow: "hidden" }}>
      <Sidebar />
      <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
        <header
          style={{
            backgroundColor: "#121212",
            padding: "12px 24px",
            display: "flex",
            alignItems: "center",
            color: "#fff",
            borderBottom: "1px solid #333",
            height: "80px",
            boxShadow: "0 2px 6px rgba(0,0,0,0.3)",
          }}
        >
          <img
            src="/onfon.jpeg"
            alt="Onfon Logo"
            style={{
              height: "60px",
              marginRight: "16px",
              display: "block",
            }}
          />
          <h1
            style={{
              fontSize: "1.8rem",
              margin: 0,
              fontWeight: "700",
              color: "#ff99aa",
              lineHeight: 1.2,
            }}
          >
            Penzi SMS Admin Dashboard
          </h1>
        </header>

        <div style={{ flex: 1, overflowY: "auto", background: "#fdfdfd" }}>
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default Layout;
