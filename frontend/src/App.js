import React from "react";
import { Routes, Route, BrowserRouter } from "react-router-dom";
import Layout from "./components/layout";
import MessageForm from "./components/MessageForm";
import Users from "./components/Users";
import Tracking from "./components/Tracking";
import SimulateSMS from "./components/SimulateSMS";
import Logistics from "./components/Logistics";
// Removed Login and PrivateRoute imports since login is not needed

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* No login route needed */}

        {/* Public routes - no PrivateRoute wrapping */}
        <Route path="/" element={<Layout />}>
          <Route path="messages" element={<MessageForm />} />
          <Route path="users" element={<Users />} />
          <Route path="tracking" element={<Tracking />} />
          <Route path="simulate" element={<SimulateSMS />} />
          <Route path="logistics" element={<Logistics />} />
          {/* Optionally, add index route to redirect or render a default component */}
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
