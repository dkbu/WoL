import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "./authContext.jsx";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL ?? "";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [mode, setMode] = useState("login"); // "login" | "register"
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      if (mode === "register") {
        const res = await fetch(`${BACKEND_URL}/api/users`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password }),
        });
        if (!res.ok) {
          const body = await res.json().catch(() => null);
          throw new Error(body?.detail ?? "Could not create account.");
        }
      }
      await login(username, password);
      navigate("/");
    } catch (err) {
      setError(err.message ?? "Something went wrong.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <section style={{ maxWidth: 320, margin: "4rem auto" }}>
      <h1>{mode === "login" ? "Log in" : "Create account"}</h1>
      <form onSubmit={handleSubmit} className="form">
        <label>
          Username
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            autoComplete="username"
          />
        </label>
        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={8}
            autoComplete={mode === "login" ? "current-password" : "new-password"}
          />
        </label>
        {error && <p role="alert" className="error-text">{error}</p>}
        <button className="button" type="submit" disabled={submitting}>
          {mode === "login" ? "Log in" : "Create account"}
        </button>
      </form>
      <button
        type="button"
        onClick={() => {
          setMode(mode === "login" ? "register" : "login");
          setError(null);
        }}
        className="link-button"
      >
        {mode === "login" ? "Need an account? Register" : "Already have an account? Log in"}
      </button>
    </section>
  );
}
