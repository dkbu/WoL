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

    fetch(`${BACKEND_URL}/api/users/${userId}/profile`)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then(setProfile)
      .catch(() => setError("Could not load this user's profile."));
  }, [userId]);

  if (error) return <p role="alert">{error}</p>;
  if (!profile) return <p>Loading profile…</p>;

  return (
    <article style={{ fontFamily: "system-ui, sans-serif" }}>
      <header style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
        {/* Stub: the backend does not yet provide profile images. */}
        <div
          aria-hidden="true"
          style={{
            width: 96,
            height: 96,
            borderRadius: "50%",
            background: "#cbd5e1",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: "2rem",
            fontWeight: 600,
            color: "#334155",
            flexShrink: 0,
          }}
        >
          {profile.user.username?.[0]?.toUpperCase() ?? "?"}
        </div>
        <div>
          <h2 style={{ margin: 0 }}>{profile.user.username}</h2>
          {profile.user.is_curator && (
            <span style={{ fontSize: "0.85rem", color: "#0f766e" }}>Curator</span>
          )}
        </div>
      </header>

      <section style={{ marginTop: "1.5rem" }}>
        <h3>About</h3>
        {/* Stub: biography is not yet implemented on the backend. */}
        <p style={{ color: "#64748b", fontStyle: "italic" }}>
          This user hasn't added a biography yet.
        </p>
      </section>

      <section style={{ marginTop: "1.5rem" }}>
        <h3>Concepts created</h3>
        {profile.created_concepts.length === 0 ? (
          <p style={{ color: "#64748b" }}>No concepts created yet.</p>
        ) : (
          <ul style={{ listStyle: "none", margin: 0, padding: 0 }}>
            {profile.created_concepts.map((concept) => (
              <ConceptCard key={concept.id} concept={concept} />
            ))}
          </ul>
        )}
      </section>

      <section style={{ marginTop: "1.5rem" }}>
        <h3>Concepts commented on</h3>
        {profile.commented_concepts.length === 0 ? (
          <p style={{ color: "#64748b" }}>No concepts commented on yet.</p>
        ) : (
          <ul style={{ listStyle: "none", margin: 0, padding: 0 }}>
            {profile.commented_concepts.map((concept) => (
              <ConceptCard key={concept.id} concept={concept} />
            ))}
          </ul>
        )}
      </section>
    </article>
  );
}
