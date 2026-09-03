import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL ?? "";

export default function CreateConcept() {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const conceptMutation = useMutation({
      mutationFn: async ({ name, description }) => {
        const res = await fetch(`${BACKEND_URL}/api/knowledge/concepts`, {
          method: "POST",
          credentials: "include",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name, description: description || null }),
        });
        if (!res.ok) {
          const body = await res.json().catch(() => null);
          throw new Error(body?.detail ?? "Could not create concept.");
        }
        return res.json();
      },
    });
  const { mutateAsync: createConcept } = conceptMutation;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      const concept = await createConcept({ name, description });
      navigate(`/concepts/${concept.id}`);
    } catch (err) {
      setError(err.message ?? "Something went wrong.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <section style={{ maxWidth: 480, margin: "2rem auto" }}>
      <h1>Create concept</h1>
      <form onSubmit={handleSubmit} className="form">
        <label>
          Name
          <input value={name} onChange={(e) => setName(e.target.value)} required />
        </label>
        <label>
          Description
          <textarea value={description} onChange={(e) => setDescription(e.target.value)} rows={4} />
        </label>
        {error && <p role="alert" className="error-text">{error}</p>}
        <div className="form-actions">
          <button className="button" type="submit" disabled={submitting}>
            Submit
          </button>
          <button className="button" type="button" onClick={() => navigate(-1)} disabled={submitting}>
            Cancel
          </button>
        </div>
      </form>
    </section>
  );
}
