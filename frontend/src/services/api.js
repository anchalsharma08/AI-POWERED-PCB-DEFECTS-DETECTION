import axios from "axios";

const api = axios.create({
    baseURL: "https://ai-powered-pcb-defects-detection.onrender.com",
});

export default api;