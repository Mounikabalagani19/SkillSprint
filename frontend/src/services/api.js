import axios from "axios";

// Force local API URL to ensure connectivity during debugging
const API_BASE = "http://localhost:8000/api/v1";

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

  loginGuest() {
    return apiClient.post("/users/guest-token");
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
  },

  getAnnouncements() {
    return apiClient.get("/announcements/");
  },

  createAnnouncement(content) {
    return apiClient.post("/announcements/", { content });
  },

  getMentorStudents() {
    return apiClient.get("/management/mentor/students");
  },

  getAdminStats() {
    return apiClient.get("/management/admin/stats");
  },

  uploadChallenges(challenges) {
    return apiClient.post("/management/mentor/challenges", challenges);
  },

  uploadPdfModule(formData) {
    return apiClient.post("/management/mentor/modules/pdf", formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },

  // --- Analytics ---
  getStudentPerformance() {
    return apiClient.get('/analytics/student-performance');
  },

  getActivityTimeline(days = 7) {
    return apiClient.get(`/analytics/activity-timeline?days=${days}`);
  }
};

