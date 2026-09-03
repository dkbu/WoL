import { Link } from "react-router-dom";
import { getConceptById, useConcepts } from "./searchData.jsx";
import ConceptThumbnail from "./conceptThumbnail.jsx";

export default function ConceptTag({ concept_id }) {
    const { data: concepts } = useConcepts();
    const conceptName = getConceptById(concepts, concept_id)?.name;
    return (
        <Link to={`/concepts/${concept_id}`}>        
            <ConceptThumbnail name={conceptName || concept_id} size={80} />
            {conceptName || concept_id}
        </Link>
    );
}