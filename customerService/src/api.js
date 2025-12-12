const API_BASE_URL = "https://intent-classification-muv8.onrender.com";

export async function predictIntent(text) {
  const res = await fetch(`${API_BASE_URL}/predict`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({}));
    throw new Error(error.detail || "Something went wrong");
  }

  return res.json();
}
