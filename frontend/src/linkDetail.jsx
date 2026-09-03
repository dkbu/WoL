import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { getConceptById, useConcepts } from "./searchData.jsx";

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
    const { data: concepts } = useConcepts();

    if (isLoading) return <p>Loading...</p>;
    if (error) return <p>Error: {error.message}</p>;

  return (
    <div>
      <h1>Link Detail Page</h1>
      <p>Source Concept: {getConceptById(concepts, link?.source_concept_id)?.name || link?.source_concept_id}</p>
      <p>Target Concept: {getConceptById(concepts, link?.target_concept_id)?.name || link?.target_concept_id}</p>
      <p>Connection: {link?.connection}</p>
    </div>
  );
}