import { useConcepts } from "./searchData.jsx";
import { useParams } from "react-router-dom";
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';

export default function CreateLink() {
  const { sourceConceptId } = useParams();
  const { data, isLoading, error } = useConcepts();

  const srcConceptName = data.find(concept => concept.id === sourceConceptId)?.name || "";

  if (isLoading) return <p>Loading…</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <section style={{ maxWidth: 480, margin: "2rem auto" }}>
      <h1>Create link</h1>
      <form className="form">
        <label>
          Source Concept
          <input type="text" value={srcConceptName} readOnly />
        </label>
        <label>
          Target Concept 
        <Autocomplete options={data} 
        getOptionLabel={(option) => option.name}
        getOptionKey={(option) => option.id}
        renderInput={(params) => (
          <TextField {...params} label="Target Concept" variant="standard" />
        )}
        />
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