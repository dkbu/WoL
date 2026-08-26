import { useEffect, useState } from "react";
import ConceptCard from "./concept.jsx";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL ?? "";

export default function UserProfile({ userId }) {
  const [profile, setProfile] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!userId) return;
    setProfile(null);
    setError(null);

    fetch(`${BACKEND_URL}/api/users/${userId}/profile`, { credentials: "include" })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then(setProfile)
      .catch(() => setError("Could not load this user's profile."));
  }, [userId]);

  if (error) return <p role="alert" className="error-text">{error}</p>;
  if (!profile) return <p>Loading profile…</p>;

  return (
    <article>
      <header style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
        {/* Stub: the backend does not yet provide profile images. */}
        <div className="avatar" aria-hidden="true">
          {profile.user.username?.[0]?.toUpperCase() ?? "?"}
        </div>
        <div>
          <h2 style={{ margin: 0 }}>{profile.user.username}</h2>
          {profile.user.is_curator && <span className="badge-curator">Curator</span>}
        </div>
      </header>

      <section className="section">
        <h3>About</h3>
        {/* Stub: biography is not yet implemented on the backend. */}
        <p className="muted italic">This user hasn't added a biography yet.</p>
      </section>

      <section className="section">
        <h3>Concepts created</h3>
        {profile.created_concepts.length === 0 ? (
          <p className="muted">No concepts created yet.</p>
        ) : (
          <ul className="list-plain">
            {profile.created_concepts.map((concept) => (
              <ConceptCard key={concept.id} concept={concept} />
            ))}
          </ul>
        )}
      </section>

      <section className="section">
        <h3>Concepts commented on</h3>
        {profile.commented_concepts.length === 0 ? (
          <p className="muted">No concepts commented on yet.</p>
        ) : (
          <ul className="list-plain">
            {profile.commented_concepts.map((concept) => (
              <ConceptCard key={concept.id} concept={concept} />
            ))}
          </ul>
        )}
      </section>
    </article>
  );
}
