import React, { useState, useEffect } from "react";
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

  const [newDoctor, setNewDoctor] = useState({ email: "", password: "", first_name: "", last_name: "", specialization: "" });
  const [newPatient, setNewPatient] = useState({ first_name: "", last_name: "", email: "", phone: "", insurance: "" });
  const [appointment, setAppointment] = useState({ patient_id: "", doctor_id: "", start_time: "", end_time: "" });

  const [availability, setAvailability] = useState({
      start_time: "",
      end_time: "",
    });

  const [patients, setPatients] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [date, setDate] = useState(null);
  const [duration, setDuration] = useState(null);
  const [slots, setSlots] = useState([]);

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

  const fetchAvailableSlots = async () => {
    if (!appointment.doctor_id || !date || !duration) {
      alert("Select doctor, date and duration first");
      return;
    }

    const res = await axios.get(`${API_BASE}/doctors/${appointment.doctor_id}/available-slots`, {
      params: { date, duration_minutes: duration },
      headers: { Authorization: `Bearer ${token}` },
    });

    setSlots(res.data);
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
        headers: { Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json' 
      }});
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

  const fetchDoctorsAndPatients = async () => {
    try {
      const patientRes = await axios.get(`${API_BASE}/patients`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const doctorRes = await axios.get(`${API_BASE}/doctors`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setPatients(patientRes.data);
      setDoctors(doctorRes.data);
    } catch (err) {
      alert("Failed to load users");
    }
  };

  useEffect(() => {
    if (token && view === "admin") {
      fetchDoctorsAndPatients();
    }
  }, [token, view]);

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
          <input placeholder="Email" value={newDoctor.email} onChange={(e) => setNewDoctor({ ...newDoctor, email: e.target.value })} />
          <input type="password" placeholder="Password" value={newDoctor.password} onChange={(e) => setNewDoctor({ ...newDoctor, password: e.target.value })} />
          <input placeholder="First Name" value={newDoctor.first_name} onChange={(e) => setNewDoctor({ ...newDoctor, first_name: e.target.value })} />
          <input placeholder="Last Name" value={newDoctor.last_name} onChange={(e) => setNewDoctor({ ...newDoctor, last_name: e.target.value })} />
          <input placeholder="Specialization" value={newDoctor.specialization} onChange={(e) => setNewDoctor({ ...newDoctor, specialization: e.target.value })} />
          <button onClick={createDoctor}>Create Doctor</button>
        </div>

        <div className="card">
          <h2>Add Patient</h2>
          <input placeholder="Email" value={newPatient.email} onChange={(e) => setNewPatient({ ...newPatient, email: e.target.value })} />
          <input type="password" placeholder="Password" value={newPatient.password} onChange={(e) => setNewPatient({ ...newPatient, password: e.target.value })} />
          <input placeholder="First Name" value={newPatient.first_name} onChange={(e) => setNewPatient({ ...newPatient, first_name: e.target.value })} />
          <input placeholder="Last Name" value={newPatient.last_name} onChange={(e) => setNewPatient({ ...newPatient, last_name: e.target.value })} />
          <input placeholder="Phone" value={newPatient.phone} onChange={(e) => setNewPatient({ ...newPatient, phone: e.target.value })} />
          <input placeholder="Insurance" value={newPatient.insurance} onChange={(e) => setNewPatient({ ...newPatient, insurance: e.target.value })} />
          <button onClick={createPatient}>Create Patient</button>
        </div>

        <div className="card">
          <h2>Schedule Appointment</h2>
          <select value={appointment.patient_id} onChange={(e) => setAppointment({ ...appointment, patient_id: e.target.value })}>
            <option value="">Select Patient</option>
            {patients.map((p) => (
              <option key={p.id} value={p.id}>{p.user.email} - {p.first_name} {p.last_name}</option>
            ))}
          </select>

          <select value={appointment.doctor_id} onChange={(e) => setAppointment({ ...appointment, doctor_id: e.target.value })}>
            <option value="">Select Doctor</option>
            {doctors.map((d) => (
              <option key={d.id} value={d.id}>{d.user.email} - {d.first_name} {d.last_name}</option>
            ))}
          </select>
          <label>Appointment Date</label>
          <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
          <input type="number" placeholder="Appointment Duration (mins)" value={duration} onChange={(e) => setDuration(Number(e.target.value))} />
          <button onClick={fetchAvailableSlots}>Get Available Slots</button>

          {slots.length > 0 && (
            <div className="slot-list">
              {slots.map((slot, idx) => (
                <button
                  key={idx}
                  className="slot-button"
                  onClick={() =>
                    setAppointment({
                      ...appointment,
                      start_time: `${date}T${slot.start}`,
                      end_time: `${date}T${slot.end}`,
                    })
                  }
                >
                  {slot.start} - {slot.end}
                </button>
              ))}
            </div>
          )}

          <button onClick={scheduleAppointment}>Schedule</button>
        </div>
      </div>
    );
  } else if (view === "doctor"){

    

    const createAvailability = async () => {
      try {
        await axios.post(`${API_BASE}/availabilities`, availability, {
          headers: { Authorization: `Bearer ${token}` },
        });
        alert("Availability saved");
        setAvailability({ start_time: "", end_time: "" });
      } catch (err) {
        alert("Failed to create availability");
      }
    };

    return (
      <div className="app-container">
        <h1>Doctor Dashboard</h1>

        <div className="card">
          <h2>Set Availability</h2>
          <label>Start Time</label>
          <input
            type="datetime-local"
            value={availability.start_time}
            onChange={(e) =>
              setAvailability({ ...availability, start_time: e.target.value })
            }
          />

          <label>End Time</label>
          <input
            type="datetime-local"
            value={availability.end_time}
            onChange={(e) =>
              setAvailability({ ...availability, end_time: e.target.value })
            }
          />

          <button onClick={createAvailability}>Save Availability</button>
        </div>
      </div>
    );
  }

  return <div className="app-container">Unsupported role view</div>;
}

export default App;
