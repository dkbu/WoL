import ConceptCard from "./concept.jsx";
import UserTag from "./userTag.jsx";
import { useConcepts, useUserSearch } from "./searchData.jsx";
import { useParams } from "react-router-dom";

export function ConceptSearchResults() {
  let { searchInput } = useParams();
  const { data: concepts, error, isLoading } = useConcepts();

  if (isLoading) return <p>Searching concepts…</p>;
  if (error) return <p role="alert" className="error-text">Could not search concepts.</p>;

  const matches = concepts.filter((concept) =>
    concept.name.toLowerCase().includes(searchInput.toLowerCase())
  );

  if (matches.length === 0) return <p className="muted">No matching concepts.</p>;

  return (
    <ul className="list-plain">
      {matches.map((concept) => (
        <ConceptCard key={concept.id} concept={concept} />
      ))}
    </ul>
  );
}

export function UserSearchResults() {
  let { searchInput } = useParams();
  const { data: users, error, isLoading } = useUserSearch(searchInput);

  if (isLoading) return <p>Searching users…</p>;
  if (error) return <p role="alert" className="error-text">Could not search users.</p>;

  if (users.length === 0) return <p className="muted">No matching users.</p>;

  return (
    <ul className="list-plain">
      {users.map((user) => (
        <li key={user.id}>
          <UserTag user={user} />
        </li>
      ))}
    </ul>
  );
}

export default function SearchResults() {
    const searchParams = new URLSearchParams(window.location.search);
    const searchInput = searchParams.get("query");
    const searchType = searchParams.get("type");

    if (!searchInput) return null;

    if (searchType === "User") return <UserSearchResults searchInput={searchInput} />;
    return <ConceptSearchResults searchInput={searchInput} />;
}
