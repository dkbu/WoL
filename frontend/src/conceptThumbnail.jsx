// Stub: the backend does not yet provide concept thumbnail images.
export default function ConceptThumbnail({ name, size = 64 }) {
  const initial = name?.trim()?.[0]?.toUpperCase() ?? "?";
  return (
    <div className="thumbnail" aria-hidden="true" style={{ width: size, height: size, fontSize: size * 0.375 }}>
      {initial}
    </div>
  );
}
