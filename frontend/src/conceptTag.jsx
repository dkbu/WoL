import { Link } from "react-router-dom";
import { getConceptById, useConcepts } from "./searchData.jsx";
import ConceptThumbnail from "./conceptThumbnail.jsx";

export default function ConceptTag({ concept_id, concept_name, linkId = null }) {
    return (
        <Link to={linkId ? `/links/${linkId}` : `/concepts/${concept_id}`}>
            <ConceptThumbnail name={concept_name || concept_id} size={80} />
            {concept_name || concept_id}
        </Link>
    );
}