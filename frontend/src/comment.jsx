import { useState } from "react";
import UserTag from "./userTag.jsx";

import { commentMutation as useCommentMutation } from "./searchData.jsx"; 

export function Comment({ comment }) {
  return (
    <p style={{ margin: "0.25rem 0" }}><UserTag user={{id: comment.creator}} />   {comment.content}</p>
  );
}

export default function CreateComment({ commentable_id, onSubmitted, onCancel }) {
  const [content, setContent] = useState("");
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const commentMutation = useCommentMutation();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      await commentMutation.mutateAsync(
        { commentContent: content, commentableId: commentable_id });
      setContent("");
      onSubmitted();
    } catch (err) {
      setError(err.message ?? "Something went wrong.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="form">
      <label>
        Content
        <textarea value={content} onChange={(e) => setContent(e.target.value)} rows={3} required />
      </label>
      {error && <p role="alert" className="error-text">{error}</p>}
      <div className="form-actions">
        <button className="button" type="submit" disabled={submitting}>
          Submit
        </button>
        <button className="button" type="button" onClick={onCancel} disabled={submitting}>
          Cancel
        </button>
      </div>
    </form>
  );
}
