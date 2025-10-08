import "./style.scss";

import { useAuth } from "@/auth";
import { API_BASE_URL } from "@/api_url";
import { useEffect, useState } from "react";
import type { FormEvent } from "react";

export default function ProfilePage() {
  const { token } = useAuth();
  const [name, setName] = useState("?");
  const [email, setEmail] = useState("?");

  useEffect(() => {
    if (!token) return;

    fetch(`${API_BASE_URL}/api/auth/me`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((response) => response.json())
      .then((data) => {
        setName(data.name);
        setEmail(data.email);
      })
      .catch((e) => {
        console.error(e);
      });
  }, [token]);

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    fetch(`${API_BASE_URL}/api/auth/update`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, name }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Invalid credentials");
        }
        return response.json();
      })
      .catch((err) => {
        alert((err as Error)?.message || "An unknown error occurred");
      });
  };

  return (
    <form className="profile-page" onSubmit={handleSubmit}>
      <h2>Profile</h2>
      <hr />
      <p>name</p>
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <p>email</p>
      <input
        type="text"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input type="submit" value="Update Profile" />
    </form>
  );
}
