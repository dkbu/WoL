import { useQuery, useMutation } from "@tanstack/react-query";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL ?? "";


export function useComments(commentable_id) {
  return useQuery({
    queryKey: ["comments", commentable_id],
    queryFn: async () => {
      const res = await fetch(`${BACKEND_URL}/api/knowledge/comments?commentable_id=${commentable_id}`, { credentials: "include" });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    },
  });
}

export function commentMutation(commentContent, commentableId) {
  return useMutation({
    mutationFn: async ({ commentContent, commentableId }) => {
      const res = await fetch(`${BACKEND_URL}/api/knowledge/comments`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ content: commentContent, commentable_id: commentableId }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    },
  });
}

export function useConceptLinks(conceptId) {
  return useQuery({
    queryKey: ["conceptLinks", conceptId],
    queryFn: async () => {
      const res = await fetch(`${BACKEND_URL}/api/knowledge/concepts/${conceptId}/links`, { credentials: "include" });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    },
  });
}

export function useConcept(conceptId) {
  return useQuery({
    queryKey: ["concept", conceptId],
    queryFn: async () => {
      const res = await fetch(`${BACKEND_URL}/api/knowledge/concepts/${conceptId}/detail`, { credentials: "include" });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    },
  });
}

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

export function getConceptById(concepts, id) {
  return concepts?.find(c => c.id === id);
}

export function getConceptNameById(concepts, id) {
  return getConceptById(concepts, id)?.name;
}

// Bundles the id/name pair ConceptTag needs, so callers can spread it directly.
export function getConceptTagProps(concepts, id, linkId = null) {
  return { concept_id: id, concept_name: getConceptNameById(concepts, id), linkId };
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

export function useUser(userId) {
  return useQuery({
    queryKey: ["users", userId],
    enabled: Boolean(userId),
    queryFn: async () => {
      const res = await fetch(`${BACKEND_URL}/api/users/${userId}`, {
        credentials: "include",
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    },
  });
}