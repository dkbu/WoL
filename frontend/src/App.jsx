import { useEffect, useState } from "react";
import { Route, Routes, useParams } from "react-router-dom";
import UserProfile from "./user.jsx";
import ConceptDetailPage from "./conceptDetail.jsx";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL ?? "";

function UserProfilePage() {
  const { userId } = useParams();
  return <UserProfile userId={userId} />;
}

function Home() {
  const [backendStatus, setBackendStatus] = useState("checking…");
  const [userId, setUserId] = useState("");
  const [viewedUserId, setViewedUserId] = useState(null);

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/health`)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data) => {
        setBackendStatus(`reachable — status: ${data.status}, db: ${data.database}`);
      })
      .catch(() => {
        setBackendStatus("unreachable");
      });
  }, []);

  return (
    <>
      <h1>Museum</h1>
      <p>A collaborative knowledge graph.</p>
      <section>
        <h2>Backend</h2>
        <p>
          Status: <strong>{backendStatus}</strong>
        </p>
      </section>
      <section>
        <h2>User profile</h2>
        <form
          onSubmit={(e) => {
            e.preventDefault();
            setViewedUserId(userId);
          }}
        >
          <label>
            User ID:{" "}
            <input value={userId} onChange={(e) => setUserId(e.target.value)} placeholder="Enter a user ID" />
          </label>
          <button type="submit">View profile</button>
        </form>
        {viewedUserId && <UserProfile userId={viewedUserId} />}
      </section>
    </>
  );
}

export default function App() {
  return (
    <main style={{ fontFamily: "system-ui, sans-serif", maxWidth: 640, margin: "4rem auto", padding: "0 1rem" }}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/concepts/:conceptId" element={<ConceptDetailPage />} />
        <Route path="/users/:userId" element={<UserProfilePage />} />
      </Routes>
    </main>
  );
}

