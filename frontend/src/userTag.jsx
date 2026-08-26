import { Link } from "react-router-dom";

const TAG_STYLE = {
  display: "inline-flex",
  alignItems: "center",
  padding: "0.15rem 0.6rem",
  borderRadius: 999,
  background: "#e2e8f0",
  color: "#1d4ed8",
  fontWeight: 600,
  fontSize: "0.9rem",
  textDecoration: "none",
};

export default function UserTag({ user }) {
  return (
    <Link to={`/users/${user.id}`} style={TAG_STYLE}>
      {user.username}
    </Link>
  );
}
