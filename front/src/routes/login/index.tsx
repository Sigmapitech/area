import type { ChangeEvent, FormEvent } from "react";
import { useState } from "react";
import { Link, useNavigate } from "react-router";

import "./auth.scss";

import { API_BASE_URL } from "@/api_url";
import { useAuth } from "@/auth";
import FormField from "@/components/form/field";
import FormSubmitButton, {
  handleFormSubmit,
} from "@/components/form/submit-button";

export default function LoginPage() {
  const { login } = useAuth();
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const REGISTRATION_FIELDS = [
    {
      label: "Email",
      name: "email",
      type: "email",
      placeholder: "Email",
      pattern: ".+@.+",
      title: "Please enter a valid email address",
    },
    {
      label: "Password",
      name: "password",
      type: "password",
      placeholder: "Password",
      pattern: ".{6,}",
      title: "Minimum 6 characters",
    },
  ];

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    setError("");

    if (!e.currentTarget.checkValidity()) return;
    e.preventDefault();

    const { email, password } = formData;

    handleFormSubmit({
      url: `${API_BASE_URL}/auth/login/`,
      body: { email, password },
      onSuccess: (data) => {
        login(data.token);
        navigate("/");
      },
      onError: (e) => {
        setError(e);
      },
    });
  };

  return (
    <div className="auth">
      <div className="auth-header">
        <h1>Login</h1>
      </div>

      <form onSubmit={handleSubmit}>
        {REGISTRATION_FIELDS.map((field) => (
          <FormField
            key={field.name}
            value={formData[field.name as keyof typeof formData]}
            onChange={handleChange}
            {...field}
          />
        ))}

        {error && <p className="error">{error}</p>}

        <div className="actions">
          <FormSubmitButton value="Sign in" />
        </div>
        <div className="info">
          <p>Don't have an account?</p>
          <Link className="btn btn-register" to="/register">
            Register
          </Link>
        </div>
      </form>
    </div>
  );
}
