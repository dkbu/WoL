import { Navigate, Route, Routes, useParams } from "react-router-dom";
import Header from "./header.jsx";
import UserProfile from "./user.jsx";
import ConceptDetailPage from "./conceptDetail.jsx";
import CreateConcept from "./createConcept.jsx";
import CreateLink from "./createLink.jsx";
import Login from "./login.jsx";
import AdminUsers from "./adminUsers.jsx";
import { AuthProvider, useAuth } from "./authContext.jsx";
import { ConceptSearchResults, UserSearchResults } from "./searchResults.jsx";

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
      <main className="page">
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
          {<Route
            path="/links/new/:sourceConceptId"
            element={
              <RequireCuratorOrAdmin>
                <Header />
                <CreateLink />
              </RequireCuratorOrAdmin>
            }
          />}
          <Route
            path="/search/concept/:searchInput"
            element={
              <RequireAuth>
                <Header />
                <ConceptSearchResults/>
              </RequireAuth>
            }
          />

          <Route
            path="/search/user/:searchInput"
            element={
              <RequireAuth>
                <Header />
                <UserSearchResults/>
              </RequireAuth>
            }
          />
        </Routes>
      </main>
    </AuthProvider>
  );
}


``