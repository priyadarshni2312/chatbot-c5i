// frontend/src/config.js
const API_BASE_URL =
  process.env.NODE_ENV === "production"
    ? "" // Empty string to use the same host
    : "http://localhost:8000"; // Local development server

export default API_BASE_URL;