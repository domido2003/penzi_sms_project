import React from "react";

function Login() {
  return (
    <div
      className="d-flex flex-column justify-content-center align-items-center vh-100"
      style={{ backgroundColor: "#ffe6f0" }}
    >
      <div
        className="p-5 rounded shadow-lg text-center"
        style={{ maxWidth: "400px", backgroundColor: "#fff" }}
      >
        <h2 className="mb-4" style={{ color: "#c71585" }}>
          Login Disabled
        </h2>
        <p className="mb-3" style={{ color: "#333", fontSize: "1.1rem" }}>
          The login functionality has been temporarily disabled for maintenance.
        </p>
        <p style={{ color: "#555" }}>
          Please check back later or contact the administrator if you need access.
        </p>
        <div
          className="mt-4"
          style={{
            fontSize: "4rem",
            color: "#c71585",
            userSelect: "none",
          }}
          aria-hidden="true"
        >
          💔
        </div>
      </div>
    </div>
  );
}

export default Login;
