import React, { useState } from "react";
import "./Register.css";
import Header from "../Header/Header";

function Register() {
  const [form, setForm] = useState({
    userName: "",
    firstName: "",
    lastName: "",
    email: "",
    password: "",
  });
  const [message, setMessage] = useState("");
  const [error, setError] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleChange = (event) => {
    setForm({ ...form, [event.target.name]: event.target.value });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setMessage("");
    setLoading(true);

    try {
      const response = await fetch(
        `${window.location.origin}/djangoapp/register`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(form),
        }
      );

      const result = await response.json();

      if (!response.ok) {
        setError(true);
        setMessage(result.error || "Registration failed. Please try again.");
        return;
      }

      setError(false);
      setMessage("Registration successful! Redirecting to login...");
      setTimeout(() => {
        window.location.href = "/login";
      }, 1200);
    } catch (err) {
      setError(true);
      setMessage("Unable to connect to the server. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Header />
      <main className="register_container">
        <h1 className="header">Register</h1>
        <form className="inputs" onSubmit={handleSubmit}>
          <input
            className="input_field"
            name="userName"
            type="text"
            placeholder="Username"
            aria-label="Username"
            value={form.userName}
            onChange={handleChange}
            required
          />
          <input
            className="input_field"
            name="firstName"
            type="text"
            placeholder="First Name"
            aria-label="First Name"
            value={form.firstName}
            onChange={handleChange}
            required
          />
          <input
            className="input_field"
            name="lastName"
            type="text"
            placeholder="Last Name"
            aria-label="Last Name"
            value={form.lastName}
            onChange={handleChange}
            required
          />
          <input
            className="input_field"
            name="email"
            type="email"
            placeholder="Email"
            aria-label="Email"
            value={form.email}
            onChange={handleChange}
            required
          />
          <input
            className="input_field"
            name="password"
            type="password"
            placeholder="Password"
            aria-label="Password"
            value={form.password}
            onChange={handleChange}
            minLength={8}
            required
          />

          {message && (
            <p role="status" style={{ color: error ? "darkred" : "darkgreen" }}>
              {message}
            </p>
          )}

          <div className="submit_panel">
            <button className="submit" type="submit" disabled={loading}>
              {loading ? "Registering..." : "Register"}
            </button>
          </div>
        </form>
        <p style={{ textAlign: "center", paddingBottom: "16px" }}>
          Already registered? <a href="/login">Login</a>
        </p>
      </main>
    </div>
  );
}

export default Register;
