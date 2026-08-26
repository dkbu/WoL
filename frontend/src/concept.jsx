import { Link } from "react-router-dom";
import ConceptThumbnail from "./conceptThumbnail.jsx";

export default function ConceptCard({ concept }) {
  return (
    <li className="list-row">
      <ConceptThumbnail name={concept.name} />
      <div>
        <Link to={`/concepts/${concept.id}`} className="list-row-title">
          {concept.name}
        </Link>
        {concept.description && <p className="muted" style={{ margin: "0.25rem 0" }}>{concept.description}</p>}
      </div>
    </li>
  );
}
