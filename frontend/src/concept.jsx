import { Link } from "react-router-dom";
import ConceptThumbnail from "./conceptThumbnail.jsx";

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
