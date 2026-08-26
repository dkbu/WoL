import { Link } from "react-router-dom";

export default function UserTag({ user }) {
  return (
    <Link to={`/users/${user.id}`} className="tag">
      {user.username}
    </Link>
  );
}
