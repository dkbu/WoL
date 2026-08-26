import { useState } from "react";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL ?? "";

export default function CreateComment({ conceptId, onSubmitted, onCancel }) {
  const [content, setContent] = useState("");
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      const res = await fetch(`${BACKEND_URL}/api/knowledge/comments`, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ commentable_id: conceptId, content }),
      });
      if (!res.ok) {
        const body = await res.json().catch(() => null);
        throw new Error(body?.detail ?? "Could not create comment.");
      }
      setContent("");
      onSubmitted();
    } catch (err) {
      setError(err.message ?? "Something went wrong.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="form">
      <label>
        Content
        <textarea value={content} onChange={(e) => setContent(e.target.value)} rows={3} required />
      </label>
      {error && <p role="alert" className="error-text">{error}</p>}
      <div className="form-actions">
        <button className="button" type="submit" disabled={submitting}>
          Submit
        </button>
        <button className="button" type="button" onClick={onCancel} disabled={submitting}>
          Cancel
        </button>
      </div>
    </form>
  );
}
