import "./style.scss";

import type { FormEvent } from "react";
import { useEffect, useState } from "react";
import { API_BASE_URL } from "@/api_url";
import { useAuth } from "@/auth";

export default function ProfilePage() {
  const { token } = useAuth();
  const [username, setUsername] = useState("?");
  const [email, setEmail] = useState("?");

  useEffect(() => {
    if (!token) return;

    fetch(`${API_BASE_URL}/api/auth/me`, {
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

    fetch(`${API_BASE_URL}/api/auth/me`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ email, username }),
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
    <form className="profile-page" onSubmit={handleSubmit}>
      <h2>Profile</h2>
      <hr />
      <p>username</p>
      <input
        type="text"
        value={username || ""}
        onChange={(e) => setUsername(e.target.value)}
      />
      <p>email</p>
      <input
        type="text"
        value={email || ""}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input type="submit" value="Update Profile" />
    </form>
  );
}
