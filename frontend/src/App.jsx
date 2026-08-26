import { Link, Navigate, Route, Routes, useParams } from "react-router-dom";
import UserProfile from "./user.jsx";
import ConceptDetailPage from "./conceptDetail.jsx";
import CreateConcept from "./createConcept.jsx";
import Login from "./login.jsx";
import AdminUsers from "./adminUsers.jsx";
import { AuthProvider, useAuth } from "./authContext.jsx";

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

function RequireCuratorOrAdmin({ children }) {
  const { user, loading } = useAuth();
  if (loading) return <p>Loading…</p>;
  if (!user) return <Navigate to="/login" replace />;
  if (!user.is_curator && !user.is_admin) return <p role="alert">Curators or admins only.</p>;
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
      <span style={{ display: "flex", gap: "0.5rem", alignItems: "center" }}>
        {(user.is_curator || user.is_admin) && (
          <Link to="/concepts/new">
            <button type="button">Create concept</button>
          </Link>
        )}
        <button type="button" onClick={logout}>
          Log out
        </button>
      </span>
    </header>
  );
}

function UserProfilePage() {
  const { userId } = useParams();
  return <UserProfile userId={userId} />;
}

function Home() {
  const { user } = useAuth();
  return <UserProfile userId={user.id} />;
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
          <Route
            path="/concepts/new"
            element={
              <RequireCuratorOrAdmin>
                <Header />
                <CreateConcept />
              </RequireCuratorOrAdmin>
            }
          />
        </Routes>
      </main>
    </AuthProvider>
  );
}


