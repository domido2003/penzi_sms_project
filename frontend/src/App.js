// src/App.js

import React from "react";
import { Routes, Route, BrowserRouter } from "react-router-dom";
import Layout from "./components/layout";
import MessageForm from "./components/MessageForm";
import Users from "./components/Users";
import Tracking from "./components/Tracking";
import SimulateSMS from "./components/SimulateSMS";
import Logistics from "./components/Logistics";
import Login from "./components/Login"; // ✅ Import login
import PrivateRoute from "./components/PrivateRoute"; // ✅ Import guard

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public route */}
        <Route path="/login" element={<Login />} />

        {/* Protected routes */}
        <Route
          path="/"
          element={
            <PrivateRoute>
              <Layout />
            </PrivateRoute>
          }
        >
          <Route path="messages" element={<MessageForm />} />
          <Route path="users" element={<Users />} />
          <Route path="tracking" element={<Tracking />} />
          <Route path="simulate" element={<SimulateSMS />} />
          <Route path="logistics" element={<Logistics />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
