import type { FormEvent } from "react";
import { useState } from "react";
import { Link, useNavigate } from "react-router";

import "./auth.scss";

import { API_BASE_URL } from "@/api_url";
import { useAuth } from "@/auth";

export default function RegisterPage() {
  const { login } = useAuth();

  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (
      !/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/.test(
        password
      )
    ) {
      setError(
        "Password must be at least 8 characters long and include uppercase, lowercase, number, and special character"
      );
      return;
    }

    fetch(`${API_BASE_URL}/api/auth/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, name, password }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Registration failed");
        }
        return response.json();
      })
      .then((data) => {
        login(data.token);
        navigate("/");
      })
      .catch((err) => {
        setError((err as Error)?.message || "An unknown error occurred");
      });
  };

  return (
    <div className="auth">
      <div className="auth-header">
        <h1>Register</h1>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="auth-box">
          <label htmlFor="email">Email</label>
          <input
            type="text"
            name="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="auth-box">
          <label htmlFor="name">Name</label>
          <input
            type="text"
            name="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div className="auth-box">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            name="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <div className="auth-box">
          <label htmlFor="confirmPassword">Confirm Password</label>
          <input
            type="password"
            name="confirmPassword"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
        </div>

        {error && <p className="error">{error}</p>}

        <div className="actions">
          <input className="btn btn-validate" type="submit" value="Sign up" />
        </div>
        <div className="info">
          <p>Already have an account?</p>
          <Link className="btn btn-login" to="/login">
            Login
          </Link>
        </div>
      </form>
    </div>
  );
}
