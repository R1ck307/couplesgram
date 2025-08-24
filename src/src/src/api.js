import axios from "axios";

const API_BASE = "http://localhost:8000";

export async function getFeed() {
  const res = await axios.get(`${API_BASE}/posts/feed`);
  return res.data;
}

export async function createPost(file, caption) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("caption", caption);
  const res = await axios.post(`${API_BASE}/posts/`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
}
