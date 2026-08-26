import { useEffect, useState } from "react";
import UserTag from "./userTag.jsx";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL ?? "";

export default function AdminUsers() {
  const [users, setUsers] = useState(null);
  const [error, setError] = useState(null);

  const loadUsers = () => {
    fetch(`${BACKEND_URL}/api/admin/users`, { credentials: "include" })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then(setUsers)
      .catch(() => setError("Could not load users."));
  };

  useEffect(loadUsers, []);

  const setRole = async (userId, role, value) => {
    setError(null);
    const res = await fetch(`${BACKEND_URL}/api/admin/users/${userId}/roles`, {
      method: "PATCH",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ [role]: value }),
    });
    if (!res.ok) {
      setError("Could not update roles.");
      return;
    }
    loadUsers();
  };

  if (error) return <p role="alert" className="error-text">{error}</p>;
  if (!users) return <p>Loading users…</p>;

  return (
    <section>
      <h2>User roles</h2>
      <table>
        <thead>
          <tr>
            <th>Username</th>
            <th>Curator</th>
            <th>Admin</th>
          </tr>
        </thead>
        <tbody>
          {users.map((u) => (
            <tr key={u.id}>
              <td><UserTag user={u} /></td>
              <td>
                <input
                  type="checkbox"
                  checked={u.is_curator}
                  onChange={(e) => setRole(u.id, "is_curator", e.target.checked)}
                />
              </td>
              <td>
                <input
                  type="checkbox"
                  checked={u.is_admin}
                  onChange={(e) => setRole(u.id, "is_admin", e.target.checked)}
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
