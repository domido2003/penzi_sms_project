import React from "react";
import Sidebar from "./Sidebar";
import Footer from "./footer";
import { Outlet, useNavigate } from "react-router-dom";

const Layout = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("accessToken");
    navigate("/login");
  };

  return (
    <div style={{ display: "flex", height: "100vh", overflow: "hidden" }}>
      <Sidebar />

      <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
        {/* Header */}
        <header
          style={{
            backgroundColor: "#121212",
            padding: "12px 24px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            color: "#fff",
            borderBottom: "1px solid #333",
            height: "80px",
            boxShadow: "0 2px 6px rgba(0,0,0,0.3)",
          }}
        >
          <div style={{ display: "flex", alignItems: "center" }}>
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
              ADMIN DASHBOARD
            </h1>
          </div>

          <button
            onClick={handleLogout}
            className="btn btn-danger btn-sm"
            style={{ padding: "6px 16px", fontSize: "14px" }}
          >
            Logout
          </button>
        </header>

        {/* Main content + footer wrapper */}
        <div style={{ flex: 1, display: "flex", flexDirection: "column", overflow: "hidden" }}>
          {/* Scrollable content */}
          <div
            style={{
              flex: 1,
              overflowY: "auto",
              padding: "20px",
              backgroundColor: "#fdfdfd",
            }}
          >
            <Outlet />
          </div>

          {/* Always visible footer */}
          <Footer />
        </div>
      </div>
    </div>
  );
};

export default Layout;
