import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1",
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

