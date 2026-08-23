import { useEffect, useState } from "react";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL ?? "";

export default function App() {
  const [backendStatus, setBackendStatus] = useState("checking…");

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
    <main style={{ fontFamily: "system-ui, sans-serif", maxWidth: 640, margin: "4rem auto", padding: "0 1rem" }}>
      <h1>Museum</h1>
      <p>A collaborative knowledge graph.</p>
      <section>
        <h2>Backend</h2>
        <p>
          Status: <strong>{backendStatus}</strong>
        </p>
      </section>
    </main>
  );
}
