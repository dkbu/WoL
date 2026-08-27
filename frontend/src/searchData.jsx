import { useQuery } from "@tanstack/react-query";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL ?? "";

export function useConcepts() {
  return useQuery({
    queryKey: ["concepts"],
    queryFn: async () => {
      const res = await fetch(`${BACKEND_URL}/api/knowledge/concepts`, {
        credentials: "include",
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    },
  });
}

export function useUserSearch(username) {
  return useQuery({
    queryKey: ["users", "search", username],
    enabled: Boolean(username),
    queryFn: async () => {
      const res = await fetch(
        `${BACKEND_URL}/api/users/search?username=${encodeURIComponent(username)}`,
        { credentials: "include" }
      );
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    },
  });
}