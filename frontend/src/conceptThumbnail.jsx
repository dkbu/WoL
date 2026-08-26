// Stub: the backend does not yet provide concept thumbnail images.
export default function ConceptThumbnail({ name, size = 64 }) {
  const initial = name?.trim()?.[0]?.toUpperCase() ?? "?";
  return (
    <div
      aria-hidden="true"
      style={{
        width: size,
        height: size,
        borderRadius: 8,
        background: "#e2e8f0",
        color: "#475569",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontSize: size * 0.375,
        fontWeight: 600,
        flexShrink: 0,
      }}
    >
      {initial}
    </div>
  );
}
