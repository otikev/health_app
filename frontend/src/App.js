import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

const API_BASE = "http://localhost:8000";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("patient");
  const [token, setToken] = useState(null);
  const [slots, setSlots] = useState([]);
  const [doctorId, setDoctorId] = useState("");
  const [date, setDate] = useState("");
  const [duration, setDuration] = useState(30);

  const login = async () => {
    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);
    try {
      const response = await axios.post(`${API_BASE}/login`, formData);
      setToken(response.data.access_token);
      alert("Login successful");
    } catch (err) {
      alert("Login failed");
    }
  };

  const register = async () => {
    try {
      await axios.post(`${API_BASE}/register`, {
        email,
        password,
        role,
      });
      alert("User registered");
    } catch (err) {
      alert("Registration failed");
    }
  };

  const fetchAvailableSlots = async () => {
    if (!doctorId || !date || !duration) {
      alert("Please fill all fields.");
      return;
    }
    try {
      const response = await axios.get(`${API_BASE}/doctors/${doctorId}/available-slots`, {
        params: {
          date,
          duration_minutes: duration,
        },
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setSlots(response.data);
    } catch (err) {
      alert("Failed to fetch slots");
    }
  };

  return (
    <div className="app-container">
      <h1>Healthcare Scheduler</h1>

      <div className="card">
        <h2>Register</h2>
        <input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input placeholder="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <select value={role} onChange={(e) => setRole(e.target.value)}>
          <option value="patient">Patient</option>
          <option value="doctor">Doctor</option>
          <option value="admin">Admin</option>
        </select>
        <button onClick={register}>Register</button>
      </div>

      <div className="card">
        <h2>Login</h2>
        <button onClick={login}>Login</button>
      </div>

      {token && (
        <div className="card">
          <h2>Find Available Slots</h2>
          <input placeholder="Doctor ID" value={doctorId} onChange={(e) => setDoctorId(e.target.value)} />
          <input placeholder="Date (YYYY-MM-DD)" value={date} onChange={(e) => setDate(e.target.value)} />
          <input type="number" placeholder="Duration (minutes)" value={duration} onChange={(e) => setDuration(e.target.value)} />
          <button onClick={fetchAvailableSlots}>Get Slots</button>

          {slots.length > 0 && (
            <ul className="slot-list">
              {slots.map((slot, idx) => (
                <li key={idx}>{slot.start} - {slot.end}</li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
