import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import UserTag from "./userTag.jsx";
import ConceptThumbnail from "./conceptThumbnail.jsx";
import CreateComment from "./comment.jsx";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL ?? "";

export default function ConceptDetailPage() {
  const { conceptId } = useParams();
  const [concept, setConcept] = useState(null);
  const [error, setError] = useState(null);
  const [showCommentForm, setShowCommentForm] = useState(false);

  const loadConcept = () => {
    fetch(`${BACKEND_URL}/api/knowledge/concepts/${conceptId}/detail`, { credentials: "include" })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then(setConcept)
      .catch(() => setError("Could not load this concept."));
  };

  useEffect(() => {
    setConcept(null);
    setError(null);
    loadConcept();
  }, [conceptId]);

  if (error) return <p role="alert" className="error-text">{error}</p>;
  if (!concept) return <p>Loading concept…</p>;

  return (
    <article>
      <p>
        <Link to="/">&larr; Back</Link>
      </p>
      <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
        <ConceptThumbnail name={concept.name} size={80} />
        <div>
          <h2 style={{ margin: 0 }}>{concept.name}</h2>
          <p className="muted" style={{ margin: "0.25rem 0 0" }}>
            Created by <UserTag user={concept.creator} />
          </p>
        </div>
      </div>
      {concept.description && <p>{concept.description}</p>}

      <section className="section">
        <h3>Linked concepts</h3>
        {concept.linked_concepts.length === 0 ? (
          <p className="muted">No linked concepts yet.</p>
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

      <section className="section">
        <h3>Comments</h3>
        {concept.comments.length === 0 ? (
          <p className="muted">No comments yet.</p>
        ) : (
          <ul className="list-plain">
            {concept.comments.map((comment) => (
              <li key={comment.id} style={{ padding: "0.5rem 0", borderBottom: "1px solid var(--color-border)" }}>
                <UserTag user={comment.creator} />
                <p style={{ margin: "0.25rem 0" }}>{comment.content}</p>
              </li>
            ))}
          </ul>
        )}

        {showCommentForm ? (
          <CreateComment
            conceptId={conceptId}
            onSubmitted={() => {
              setShowCommentForm(false);
              loadConcept();
            }}
            onCancel={() => setShowCommentForm(false)}
          />
        ) : (
          <button className="button" type="button" onClick={() => setShowCommentForm(true)}>
            Add comment
          </button>
        )}
      </section>
    </article>
  );
}
