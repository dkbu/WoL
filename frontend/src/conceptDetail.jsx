import { useState } from "react";
import { Link, useParams } from "react-router-dom";
import UserTag from "./userTag.jsx";
import ConceptThumbnail from "./conceptThumbnail.jsx";
import CreateComment from "./comment.jsx";
import { useConceptLinks, useConcept, useConcepts, getConceptTagProps } from "./searchData.jsx";
import ConceptTag from "./conceptTag.jsx";

export default function ConceptDetailPage() {
  const { conceptId } = useParams();
  const { data: concept, isLoading: conceptIsLoading, error: conceptError } = useConcept(conceptId);
  const [showCommentForm, setShowCommentForm] = useState(false);
  const { data: conceptLinks, isLoading, error: conceptLinksError } = useConceptLinks(conceptId);
  const { data: concepts } = useConcepts();

  if (conceptError) return <p role="alert" className="error-text">{conceptError}</p>;
  if (conceptIsLoading) return <p>Loading concept…</p>;

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
        {conceptLinksError && <p role="alert" className="error-text">{conceptLinksError}</p>}
        {isLoading && <p>Loading linked concepts…</p>}
        {!conceptLinks || conceptLinks.length === 0 ? (
          <p className="muted">No linked concepts yet.</p>
        ) : (
          <ul>
            {conceptLinks.map((linked) => (
              <li key={linked.id}>
                <Link to={`links/${linked.id}`}>
                  <ConceptTag {...getConceptTagProps(concepts, linked.target_concept_id, linked.id)} />
                </Link>
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
