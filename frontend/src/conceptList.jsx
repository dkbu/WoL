import { useEffect, useState } from "react";
import ConceptCard from "./concept.jsx";
import { useConcepts } from "./searchData.jsx";


export default function ConceptList({ userId }) {
  const [error, setError] = useState(null);


  const { data: concepts, error: queryError, isLoading } = useConcepts();

  useEffect(() => {
    if (queryError) setError("Could not load concept list.");
  }, [queryError]);

  if (error) return <p role="alert" className="error-text">{error}</p>;
  if (isLoading) return <p>Loading concepts…</p>;

  return (
    <article>
      <section className="section">
        <h1>Concepts</h1>
        {concepts.length === 0 ? (
          <p className="muted">No concepts created yet.</p>
        ) : (
          <ul className="list-plain">
            {concepts.map((concept) => (
              <ConceptCard key={concept.id} concept={concept} />
            ))}
          </ul>
        )}
      </section>
    </article>
  );
}