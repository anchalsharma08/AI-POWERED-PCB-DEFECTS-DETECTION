import axios from "axios";

const api = axios.create({
    baseURL: "https://ai-powered-pcb-defects-detection-production.up.railway.app",
});

export default api;