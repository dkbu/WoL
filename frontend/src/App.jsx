import { useEffect, useState } from "react";
import { Link, Navigate, Route, Routes, useParams } from "react-router-dom";
import UserProfile from "./user.jsx";
import ConceptDetailPage from "./conceptDetail.jsx";
import Login from "./login.jsx";
import AdminUsers from "./adminUsers.jsx";
import { AuthProvider, useAuth } from "./authContext.jsx";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL ?? "";

function RequireAuth({ children }) {
  const { user, loading } = useAuth();
  if (loading) return <p>Loading…</p>;
  if (!user) return <Navigate to="/login" replace />;
  return children;
}

function RequireAdmin({ children }) {
  const { user, loading } = useAuth();
  if (loading) return <p>Loading…</p>;
  if (!user) return <Navigate to="/login" replace />;
  if (!user.is_admin) return <p role="alert">Admins only.</p>;
  return children;
}

function Header() {
  const { user, logout } = useAuth();
  if (!user) return null;
  return (
    <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
      <span>
        Logged in as <strong>{user.username}</strong>
        {user.is_curator && " (curator)"}
        {user.is_admin && " (admin)"}
        {user.is_admin && (
          <>
            {" "}
            · <Link to="/admin">Manage users</Link>
          </>
        )}
      </span>
      <button type="button" onClick={logout}>
        Log out
      </button>
    </header>
  );
}

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
    <AuthProvider>
      <main style={{ fontFamily: "system-ui, sans-serif", maxWidth: 640, margin: "4rem auto", padding: "0 1rem" }}>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/"
            element={
              <RequireAuth>
                <Header />
                <Home />
              </RequireAuth>
            }
          />
          <Route
            path="/concepts/:conceptId"
            element={
              <RequireAuth>
                <Header />
                <ConceptDetailPage />
              </RequireAuth>
            }
          />
          <Route
            path="/users/:userId"
            element={
              <RequireAuth>
                <Header />
                <UserProfilePage />
              </RequireAuth>
            }
          />
          <Route
            path="/admin"
            element={
              <RequireAdmin>
                <Header />
                <AdminUsers />
              </RequireAdmin>
            }
          />
        </Routes>
      </main>
    </AuthProvider>
  );
}


