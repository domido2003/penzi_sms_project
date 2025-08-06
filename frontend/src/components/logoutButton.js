import React from "react";
import { useNavigate } from "react-router-dom";

function LogoutButton() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("accessToken");
    navigate("/login");
  };

  return (
    <button
      onClick={handleLogout}
      className="btn btn-danger btn-sm"
      style={{ padding: "6px 14px", fontSize: "14px" }}
    >
      Logout
    </button>
  );
}

export default LogoutButton;

