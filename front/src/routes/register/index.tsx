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

export default function RegisterPage() {
  const { login } = useAuth();
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    email: "",
    name: "",
    password: "",
    confirmPassword: "",
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
      label: "Name",
      name: "name",
      type: "text",
      placeholder: "Name",
      pattern: ".*",
      title: "Please enter your name",
    },
    {
      label: "Password",
      name: "password",
      type: "password",
      placeholder: "Password",
      pattern:
        "^(?=.*[a-z])(?=.*[A-Z])(?=.*d)(?=.*[@$!%*?&])[A-Za-zd@$!%*?&]{8,}$",
      title:
        "Password must be at least 8 characters long and include uppercase, lowercase, number, and special character",
    },
    {
      label: "Confirm Password",
      name: "confirmPassword",
      type: "password",
      placeholder: "Confirm Password",
      pattern:
        "^(?=.*[a-z])(?=.*[A-Z])(?=.*d)(?=.*[@$!%*?&])[A-Za-zd@$!%*?&]{8,}$",
      title:
        "Password must be at least 8 characters long and include uppercase, lowercase, number, and special character",
    },
  ];

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;

    setFormData((prev) => {
      const next = { ...prev, [name]: value };

      if (name === "password" || name === "confirmPassword") {
        if (next.password !== next.confirmPassword)
          setError("Passwords do not match");
        else setError("");
      }

      return next;
    });

    console.log(name);
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    setError("");

    if (!e.currentTarget.checkValidity()) return;
    e.preventDefault();

    const { email, name, password, confirmPassword } = formData;

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    handleFormSubmit({
      url: `${API_BASE_URL}/auth/register/`,
      body: { email, name, password },
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
        <h1>Register</h1>
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
          <FormSubmitButton value="Sign up" />
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
