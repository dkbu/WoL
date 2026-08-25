import { Link } from "react-router-dom";

const THUMBNAIL_STYLE = {
  width: 64,
  height: 64,
  borderRadius: 8,
  background: "#e2e8f0",
  color: "#475569",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  fontSize: "1.5rem",
  fontWeight: 600,
  flexShrink: 0,
};

// Stub: the backend does not yet provide concept thumbnail images.
function ConceptThumbnail({ name }) {
  const initial = name?.trim()?.[0]?.toUpperCase() ?? "?";
  return (
    <div style={THUMBNAIL_STYLE} aria-hidden="true">
      {initial}
    </div>
  );
}

export default function ConceptCard({ concept }) {
  return (
    <li
      style={{
        display: "flex",
        gap: "1rem",
        alignItems: "center",
        padding: "0.75rem 0",
        borderBottom: "1px solid #e2e8f0",
      }}
    >
      <ConceptThumbnail name={concept.name} />
      <div>
        <Link to={`/concepts/${concept.id}`} style={{ fontWeight: 600, color: "#1d4ed8" }}>
          {concept.name}
        </Link>
        {concept.description && (
          <p style={{ margin: "0.25rem 0", color: "#475569" }}>{concept.description}</p>
        )}
      </div>
    </li>
  );
}
