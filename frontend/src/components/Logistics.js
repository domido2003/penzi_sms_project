import React, { useEffect, useState } from "react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  LineChart, Line, ResponsiveContainer
} from "recharts";
import axios from "axios";
import "./Logistics.css";

function Logistics() {
  const [userGrowth, setUserGrowth] = useState([]);
  const [messageVolume, setMessageVolume] = useState([]);
  const [topCounties, setTopCounties] = useState([]);
  const [descriptionVolume, setDescriptionVolume] = useState([]);

  useEffect(() => {
    fetchUserGrowth();
    fetchMessageVolume();
    fetchTopCounties();
    fetchDescriptionVolume();
  }, []);

  const fetchUserGrowth = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/api/stats/user-growth/");
      setUserGrowth(res.data);
    } catch (error) {
      console.error("User growth fetch failed", error);
    }
  };

  const fetchMessageVolume = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/api/stats/message-volume/");
      setMessageVolume(res.data);
    } catch (error) {
      console.error("Message volume fetch failed", error);
    }
  };

  const fetchTopCounties = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/api/stats/top-counties/");
      setTopCounties(res.data);
    } catch (error) {
      console.error("Top counties fetch failed", error);
    }
  };

  const fetchDescriptionVolume = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/api/stats/description-volume/");
      setDescriptionVolume(res.data);
    } catch (error) {
      console.error("Description volume fetch failed", error);
    }
  };

  const ChartCard = ({ title, children }) => (
    <div className="chart-card vibrant-glass animate-fade-in">
      <h4 className="chart-title">{title}</h4>
      <div className="chart-container">{children}</div>
    </div>
  );

  return (
    <div className="logistics-wrapper">
      <div className="page-header animate-fade-in">
        <h2>💡 Logistics & Insights Dashboard</h2>
        <div className="status-indicator">
          <span className="pulse-dot" /> Active
        </div>
      </div>

      <div className="charts-grid">
        <ChartCard title="📈 User Registrations Over Time">
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={userGrowth}>
              <CartesianGrid stroke="#ddd" strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="users" stroke="#FF4081" strokeWidth={4} dot={{ r: 5 }} />
            </LineChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="📬 Message Volume Over Time">
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={messageVolume}>
              <CartesianGrid stroke="#ccc" strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="messages" fill="#42A5F5" />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="🌍 Top Counties by User Count">
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={topCounties}>
              <CartesianGrid stroke="#bbb" strokeDasharray="3 3" />
              <XAxis dataKey="county" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="count" fill="#66BB6A" />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="🗣️ Self-Descriptions Submitted">
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={descriptionVolume}>
              <CartesianGrid stroke="#aaa" strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="count" fill="#AB47BC" />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>
    </div>
  );
}

export default Logistics;
