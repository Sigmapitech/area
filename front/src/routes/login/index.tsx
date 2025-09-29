import type { FormEvent } from "react";
import { useState } from "react";
import { Link, useNavigate } from "react-router";

import "./auth.scss";
import { useAuth } from "@/auth";

const API_BASE_URL = "http://127.0.0.1:8000";

export default function LoginPage() {
  const { login } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");

    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        throw new Error("Invalid credentials");
      }

      const data = await response.json();

            login(data.token);
      navigate("/");
    } catch (err) {
      setError(err?.message);
    }
  };

  return (
    <div className="auth">
      <div className="auth-header">
        <h1>Login</h1>
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
          <label htmlFor="password">Password</label>
          <input
            type="password"
            name="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        {error && <p className="error">{error}</p>}

        <div className="actions">
          <input className="btn btn-validate" type="submit" value="Sign in" />
        </div>
      </form>
    </div>
  );
}
