import { useAuth } from "./authContext.jsx";
import { useNavigate, Link } from "react-router-dom";
import { useState } from "react";

export default function Header() {
  const { user, logout } = useAuth();
  const [searchInput, setSearchInput] = useState("");
  const [searchType, setSearchType] = useState("Concept");
  const navigate = useNavigate();

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    navigate(`/search/${searchType.toLowerCase()}/${encodeURIComponent(searchInput)}`);
  };

  if (!user) return null;
  return (
    <>
      <header className="header">
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
        <span className="header-actions">
          {(user.is_curator || user.is_admin) && (
            <Link to="/concepts/new">
              <button className="button" type="button">Create concept</button>
            </Link>
          )}
          <form className="searchField" onSubmit={handleSearchSubmit}>
            <input
              type="text"
              placeholder="Search..."
              className="searchInput"
              value={searchInput}
              onChange={(e) => setSearchInput(e.target.value)}
            />
            <select
              id="search-type"
              className="searchType"
              value={searchType}
              onChange={(e) => setSearchType(e.target.value)}
            >
              <option value="Concept">Concept</option>
              <option value="User">User</option>
            </select>
            <input type="submit" value="Search" />
          </form> 
          <button className="button" type="button" onClick={logout}>
            Log out
          </button>
        </span>
      </header>
    </>
  );
}