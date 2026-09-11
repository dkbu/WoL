import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import ConceptTag from "./conceptTag.jsx";
import { useConcepts, useUser, getConceptTagProps } from "./searchData.jsx";
import { Link } from "react-router-dom";
import UserTag from "./userTag.jsx";
import CommentSection from "./commentSection.jsx";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL ?? "";

export function useLink(linkId) {
    return useQuery({
    queryKey: ["link", linkId],
    queryFn: async () => {
        const url = `${BACKEND_URL}/api/knowledge/links/${linkId}`;
      const res = await fetch(url, {
        credentials: "include",
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    },
  });
}

export default function LinkDetail() {
    const { linkId } = useParams();

    const { data: link, isLoading, error } = useLink(linkId);
    const { data: creator } = useUser(link?.creator_id);
    const { data: concepts } = useConcepts();

    if (isLoading) return <p>Loading...</p>;
    if (error) return <p>Error: {error.message}</p>;
  return (
    <article>
      <p>
        <Link to="/">&larr; Back</Link>
      </p>
      <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
        <ConceptTag {...getConceptTagProps(concepts, link?.source_concept_id)} size={80} />
        and
        <ConceptTag {...getConceptTagProps(concepts, link?.target_concept_id)} size={80} />
        <div>
            Created by {creator && <UserTag user={creator} />}
        </div>
      </div>
      <section>
        <p>{link?.connection}</p>
      </section>
      
            <CommentSection 
              commentable_id={linkId}
            />
      </article>
  );
}