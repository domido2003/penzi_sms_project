// src/App.js

import React from "react";
import { Routes, Route } from "react-router-dom";
import Layout from "./components/layout";
import MessageForm from "./components/MessageForm";
import Users from "./components/Users";
import Tracking from "./components/Tracking";
import SimulateSMS from "./components/SimulateSMS";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route path="/messages" element={<MessageForm />} />
        <Route path="/users" element={<Users />} />
        <Route path="/tracking" element={<Tracking />} />
        <Route path="/simulate" element={<SimulateSMS />} />
      </Route>
    </Routes>
  );
}

export default App;
