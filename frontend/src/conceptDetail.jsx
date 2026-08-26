import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import UserTag from "./userTag.jsx";
import ConceptThumbnail from "./conceptThumbnail.jsx";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL ?? "";

export default function ConceptDetailPage() {
  const { conceptId } = useParams();
  const [concept, setConcept] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    setConcept(null);
    setError(null);

    fetch(`${BACKEND_URL}/api/knowledge/concepts/${conceptId}/detail`, { credentials: "include" })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then(setConcept)
      .catch(() => setError("Could not load this concept."));
  }, [conceptId]);

  if (error) return <p role="alert">{error}</p>;
  if (!concept) return <p>Loading concept…</p>;

  return (
    <article style={{ fontFamily: "system-ui, sans-serif" }}>
      <p>
        <Link to="/">&larr; Back</Link>
      </p>
      <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
        <ConceptThumbnail name={concept.name} size={80} />
        <div>
          <h2 style={{ margin: 0 }}>{concept.name}</h2>
          <p style={{ color: "#64748b", margin: "0.25rem 0 0" }}>
            Created by <UserTag user={concept.creator} />
          </p>
        </div>
      </div>
      {concept.description && <p>{concept.description}</p>}

      <section style={{ marginTop: "1.5rem" }}>
        <h3>Linked concepts</h3>
        {concept.linked_concepts.length === 0 ? (
          <p style={{ color: "#64748b" }}>No linked concepts yet.</p>
        ) : (
          <ul>
            {concept.linked_concepts.map((linked) => (
              <li key={linked.id}>
                <Link to={`/concepts/${linked.id}`}>{linked.name}</Link>
              </li>
            ))}
          </ul>
        )}
      </section>

      <section style={{ marginTop: "1.5rem" }}>
        <h3>Comments</h3>
        {concept.comments.length === 0 ? (
          <p style={{ color: "#64748b" }}>No comments yet.</p>
        ) : (
          <ul style={{ listStyle: "none", margin: 0, padding: 0 }}>
            {concept.comments.map((comment) => (
              <li key={comment.id} style={{ padding: "0.5rem 0", borderBottom: "1px solid #e2e8f0" }}>
                <UserTag user={comment.creator} />
                <p style={{ margin: "0.25rem 0" }}>{comment.content}</p>
              </li>
            ))}
          </ul>
        )}
      </section>
    </article>
  );
}
