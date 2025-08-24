import React, { useState, useEffect } from "react";
import { getFeed, createPost } from "./api";

function App() {
  const [feed, setFeed] = useState([]);
  const [file, setFile] = useState(null);
  const [caption, setCaption] = useState("");

  useEffect(() => {
    async function fetchFeed() {
      const data = await getFeed();
      setFeed(data);
    }
    fetchFeed();
  }, []);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return alert("Select a file first!");
    await createPost(file, caption);
    setFile(null);
    setCaption("");
    const data = await getFeed();
    setFeed(data);
  };

  return (
    <div className="container">
      <h1>CouplesGram</h1>
      <form onSubmit={handleUpload}>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <input
          type="text"
          placeholder="Caption..."
          value={caption}
          onChange={(e) => setCaption(e.target.value)}
        />
        <button type="submit">Upload</button>
      </form>
      <div className="feed">
        {feed.map((post) => (
          <div key={post.id} className="post">
            {post.type === "image" ? (
              <img src={`http://localhost:8000/${post.file_path}`} alt="" />
            ) : (
              <video src={`http://localhost:8000/${post.file_path}`} controls />
            )}
            <p>{post.caption}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
