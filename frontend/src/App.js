// File: src/App.jsx
import React, { useState } from "react";
import axios from "axios";
import "./App.css";

const API_BASE = "http://localhost:8000";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("admin");
  const [token, setToken] = useState(null);
  const [userRole, setUserRole] = useState(null);
  const [view, setView] = useState("login");

  const [newDoctor, setNewDoctor] = useState({ first_name: "", last_name: "", specialization: "" });
  const [newPatient, setNewPatient] = useState({ first_name: "", last_name: "", email: "", phone: "", insurance: "" });
  const [appointment, setAppointment] = useState({ patient_id: "", doctor_id: "", start_time: "", end_time: "" });

  const login = async () => {
    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);
    try {
      const response = await axios.post(`${API_BASE}/login`, formData);
      setToken(response.data.access_token);
      setUserRole(role);
      setView(role); // Simplified for now
    } catch (err) {
      alert("Login failed");
    }
  };

  const register = async () => {
    try {
      await axios.post(`${API_BASE}/register`, { email, password, role });
      alert("User registered");
    } catch (err) {
      alert("Registration failed");
    }
  };

  const createDoctor = async () => {
    try {
      await axios.post(`${API_BASE}/doctors`, newDoctor, {
        headers: { Authorization: `Bearer ${token}` },
      });
      alert("Doctor created");
    } catch (err) {
      alert("Failed to create doctor");
    }
  };

  const createPatient = async () => {
    try {
      await axios.post(`${API_BASE}/patients`, newPatient, {
        headers: { Authorization: `Bearer ${token}` },
      });
      alert("Patient created");
    } catch (err) {
      alert("Failed to create patient");
    }
  };

  const scheduleAppointment = async () => {
    try {
      await axios.post(`${API_BASE}/appointments`, appointment, {
        headers: { Authorization: `Bearer ${token}` },
      });
      alert("Appointment scheduled");
    } catch (err) {
      alert("Failed to schedule appointment");
    }
  };

  if (!token) {
    return (
      <div className="app-container">
        <h1>Login</h1>
        <input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <select value={role} onChange={(e) => setRole(e.target.value)}>
          <option value="admin">Admin</option>
          <option value="doctor">Doctor</option>
          <option value="patient">Patient</option>
        </select>
        <button onClick={login}>Login</button>
      </div>
    );
  }

  if (view === "admin") {
    return (
      <div className="app-container">
        <h1>Admin Dashboard</h1>

        <div className="card">
          <h2>Add Doctor</h2>
          <input placeholder="First Name" value={newDoctor.first_name} onChange={(e) => setNewDoctor({ ...newDoctor, first_name: e.target.value })} />
          <input placeholder="Last Name" value={newDoctor.last_name} onChange={(e) => setNewDoctor({ ...newDoctor, last_name: e.target.value })} />
          <input placeholder="Specialization" value={newDoctor.specialization} onChange={(e) => setNewDoctor({ ...newDoctor, specialization: e.target.value })} />
          <button onClick={createDoctor}>Create Doctor</button>
        </div>

        <div className="card">
          <h2>Add Patient</h2>
          <input placeholder="First Name" value={newPatient.first_name} onChange={(e) => setNewPatient({ ...newPatient, first_name: e.target.value })} />
          <input placeholder="Last Name" value={newPatient.last_name} onChange={(e) => setNewPatient({ ...newPatient, last_name: e.target.value })} />
          <input placeholder="Email" value={newPatient.email} onChange={(e) => setNewPatient({ ...newPatient, email: e.target.value })} />
          <input placeholder="Phone" value={newPatient.phone} onChange={(e) => setNewPatient({ ...newPatient, phone: e.target.value })} />
          <input placeholder="Insurance" value={newPatient.insurance} onChange={(e) => setNewPatient({ ...newPatient, insurance: e.target.value })} />
          <button onClick={createPatient}>Create Patient</button>
        </div>

        <div className="card">
          <h2>Schedule Appointment</h2>
          <input placeholder="Patient ID" value={appointment.patient_id} onChange={(e) => setAppointment({ ...appointment, patient_id: e.target.value })} />
          <input placeholder="Doctor ID" value={appointment.doctor_id} onChange={(e) => setAppointment({ ...appointment, doctor_id: e.target.value })} />
          <input placeholder="Start Time (ISO)" value={appointment.start_time} onChange={(e) => setAppointment({ ...appointment, start_time: e.target.value })} />
          <input placeholder="End Time (ISO)" value={appointment.end_time} onChange={(e) => setAppointment({ ...appointment, end_time: e.target.value })} />
          <button onClick={scheduleAppointment}>Schedule</button>
        </div>
      </div>
    );
  }

  return <div className="app-container">Unsupported role view</div>;
}

export default App;
