import "./style.scss";

import type { FormEvent } from "react";
import { useEffect, useState } from "react";
import { API_BASE_URL } from "@/api_url";
import { useAuth } from "@/auth";

export default function ProfilePage() {
  const { token, logout } = useAuth();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [originalEmail, setOriginalEmail] = useState(""); // track original
  const [password, setPassword] = useState("");
  const [currentPassword, setCurrentPassword] = useState("");

  useEffect(() => {
    if (!token) return;

    fetch(`${API_BASE_URL}/auth/me`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch profile");
        return res.json();
      })
      .then((data) => {
        setName(data.name || "");
        setEmail(data.email || "");
        setOriginalEmail(data.email || "");
      })
      .catch((err) => {
        alert((err as Error)?.message || "An unknown error occurred");
      });
  }, [token]);

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!token) {
      alert("You must be logged in to update your profile");
      return;
    }

    const payload: Record<string, string> = {};

    if (name !== "") payload.name = name;

    if (email !== originalEmail) {
      if (!currentPassword) {
        alert("Changing your email requires entering your current password.");
        return;
      }
      payload.email = email;
      payload.current_password = currentPassword;
    }

    if (password && currentPassword) {
      payload.password = password;
      payload.current_password = currentPassword;
    } else if (password && !currentPassword) {
      alert("To change your password, enter your current password.");
      return;
    }

    if (Object.keys(payload).length === 0) {
      alert("Nothing to update.");
      return;
    }

    fetch(`${API_BASE_URL}/auth/credentials`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(payload),
    })
      .then((res) => {
        if (!res.ok) throw new Error(`Error ${res.status}: ${res.statusText}`);
        return res.json();
      })
      .then((data) => {
        alert("Profile updated successfully!");
        setName(data.name || name);
        setEmail(data.email || email);
        setOriginalEmail(data.email || email);
        setPassword("");
        setCurrentPassword("");
      })
      .catch((err) => {
        alert((err as Error)?.message || "An unknown error occurred");
      });
  };

  return (
    <div className="profile-wrapper">
      <div className="profile-container">
        <h1>Profile</h1>
        <form className="profile-form" onSubmit={handleSubmit}>
          <input
            placeholder="Name"
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <input
            placeholder="Email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <hr style={{ width: "100%", opacity: 0.3 }} />

          <input
            placeholder="Current Password"
            type="password"
            value={currentPassword}
            onChange={(e) => setCurrentPassword(e.target.value)}
          />
          <input
            placeholder="New Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button className="btn" type="submit">
            Update Profile
          </button>
        </form>
        <button className="btn" type="button" onClick={logout}>
          Logout
        </button>
      </div>
    </div>
  );
}
