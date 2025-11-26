import axios from "axios";

// Prefer env-configured API base; fallback to deployed Render backend URL
const API_BASE = import.meta.env.VITE_API_URL || "https://skillsprint-yb1p.onrender.com/api/v1";

const apiClient = axios.create({
  baseURL: API_BASE,
});

// Interceptor to add the auth token to every request
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default {
  getChallenges() {
    return apiClient.get("/challenges/");
  },

  createUser(userData) {
    return apiClient.post("/users/", userData);
  },

  loginUser(formData) {
    return apiClient.post("/users/token", formData, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });
  },

  submitAnswer(challengeId, answer) {
    return apiClient.post(`/challenges/${challengeId}/submit`, { answer });
  },

  getLeaderboard() {
    return apiClient.get("/leaderboard/");
  },

  // --- NEW FUNCTION TO GET USER'S OWN DATA ---
  getMe() {
    return apiClient.get('/users/me');
  },

  // --- Modules ---
  listModuleLevels() {
    return apiClient.get('/modules/levels');
  },

  getModuleItems(level, module = 'python') {
    if (module && module !== 'python') return apiClient.get(`/modules/${module}/${level}`);
    return apiClient.get(`/modules/${level}`); // back-compat
  },

  submitModuleAnswer(level, payload, module = 'python') {
    if (module && module !== 'python') return apiClient.post(`/modules/${module}/${level}/submit`, payload);
    return apiClient.post(`/modules/${level}/submit`, payload); // back-compat
  }
};

