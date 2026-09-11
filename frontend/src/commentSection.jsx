import { useComments } from "./searchData.jsx";
import { useState } from "react";
import { useAuth } from "./searchData.jsx";
import UserTag from "./userTag.jsx";
import CreateComment from "./comment.jsx";
import Comment from "./comment.jsx";

export default function CommentSection({ commentable_id, user }) {
    const { data: comments, isLoading, error } = useComments(commentable_id);
    const [showCommentForm, setShowCommentForm] = useState(false);

    return (
<section className="section">
        <h3>Comments</h3>
        {isLoading ? (
          <p>Loading...</p>
        ) : error ? (
          <p>Error: {error.message}</p>
        ) : comments.length === 0 ? (
          <p className="muted">No comments yet.</p>
        ) : (
          <ul className="list-plain">
            {comments.map((comment) => (
              <li key={comment.id} style={{ padding: "0.5rem 0", borderBottom: "1px solid var(--color-border)" }}>
                <UserTag user={{id: comment.creator}} />
                <Comment comment={comment} />
              </li>
            ))}
          </ul>
        )}

        {showCommentForm ? (
          <CreateComment
            creator={user.id}
            commentable_id={commentable_id}
            onSubmitted={() => {
              setShowCommentForm(false);
            }}
            onCancel={() => setShowCommentForm(false)}
          />
        ) : (
          <button className="button" type="button" onClick={() => setShowCommentForm(true)}>
            Add comment
          </button>
        )}
      </section>
    );
}