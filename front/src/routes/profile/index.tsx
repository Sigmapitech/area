import "./style.scss";

import type { FormEvent } from "react";
import { useEffect, useState } from "react";
import { API_BASE_URL } from "@/api_url";
import { useAuth } from "@/auth";

export default function ProfilePage() {
  const { token } = useAuth();
  const [name, setUsername] = useState("?");
  const [email, setEmail] = useState("?");

  useEffect(() => {
    if (!token) return;

    fetch(`${API_BASE_URL}/auth/me`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((response) => response.json())
      .then((data) => {
        setUsername(data.name);
        setEmail(data.email);
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
    console.log(JSON.stringify({ email, name }));
    fetch(`${API_BASE_URL}/auth/me`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ email, name }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Error ${response.status}: ${response.statusText}`);
        }
        return response.json();
      })
      .then((data) => {
        alert("Profile updated successfully!");
        setUsername(data.name);
        setEmail(data.email);
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
            required
            type="text"
            value={name || ""}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            placeholder="Email"
            required
            type="email"
            value={email || ""}
            onChange={(e) => setEmail(e.target.value)}
          />
          <button type="submit">Update Profile</button>
        </form>
      </div>
    </div>
  );
}
