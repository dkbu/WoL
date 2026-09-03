import { getConceptById, useConcepts } from "./searchData.jsx";
import { useParams, useNavigate } from "react-router-dom";
import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL ?? "";
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';
import { useAuth } from "./authContext.jsx";

export default function CreateLink() {
  const { sourceConceptId } = useParams();
  const [targetConceptId, setTargetConceptId] = useState(null);
  const [connection, setConnection] = useState("");
  
  const { user } = useAuth();
  let navigate = useNavigate();

  const { data: concepts, isLoading: conceptsLoading, error: conceptsError } = useConcepts();
  const srcConceptName = getConceptById(concepts, sourceConceptId)?.name || "";
  const filteredConcepts = concepts?.filter(concept => concept.id !== sourceConceptId) ?? [];

  const linkMutation = useMutation({
      mutationFn: async ({ sourceConceptId, targetConceptId, creatorId, connection }) => {
        const res = await fetch(`${BACKEND_URL}/api/knowledge/concept-links`, {
          method: "POST",
          credentials: "include",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ source_concept_id: sourceConceptId, target_concept_id: targetConceptId, creator_id: creatorId, connection: connection }),
        });
        if (!res.ok) {
          const body = await res.json().catch(() => null);
          throw new Error(body?.detail ?? "Could not create link.");
        }
        return res.json();
      },
    });
  const { mutateAsync: createLink } = linkMutation;

  const { isLoading: linkLoading, error: linkError } = linkMutation;
  if (conceptsLoading || linkLoading) return <p>Loading…</p>;
  if (conceptsError) return <p>Error: {conceptsError.message}</p>;
  if (linkError) return <p>Error: {linkError.message}</p>;

  const onSubmit = async (event) => {
    event.preventDefault();
    const newLink = await createLink({ sourceConceptId, targetConceptId, creatorId: user.id, connection });
    navigate(`/links/${newLink.id}`); // Redirect after submission
  };

  return (
    <section style={{ maxWidth: 480, margin: "2rem auto" }}>
      <h1>Create link</h1>
      <form className="form" onSubmit={onSubmit}>
        <label>
          Source Concept
          <input type="text" value={srcConceptName} readOnly />
        </label>
        <label>
          Target Concept 
        <Autocomplete 
          name="selectTargetConcept"
          options={filteredConcepts}
          getOptionLabel={(option) => option.name}
          getOptionKey={(option) => option.id}
          onChange={(_, value) => setTargetConceptId(value?.id ?? null)}
          renderInput={(params) => (
            <TextField {...params} label="Target Concept" variant="standard" />
          )}
        />
        </label>
        <label>
          Connection 
          <input type="text" name="connection" value={connection} onChange={(e) => setConnection(e.target.value)} />
        </label>
        <div className="form-actions">
          <button className="button" type="submit">
            Submit
          </button>
        </div>
      </form>
    </section>
  );
}