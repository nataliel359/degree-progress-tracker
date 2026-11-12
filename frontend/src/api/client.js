import axios from "axios";

const API = axios.create({
    baseURL: process.env.REACT_APP_API_URL || "http://127.0.0.1:8000"
});

API.interceptors.request.use((config) => {
    const token = localStorage.getItem("token");

    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
});

export const loginUser = async (credentials) => {
    const response = await API.post("/auth/login", credentials);
    return response.data;
};

export const registerUser = async (userData) => {
    const response = await API.post("/auth/register", userData);
    return response.data;
};

export const getCurrentUser = async () => {
    const response = await API.get("/auth/me");
    return response.data;
};

export const requestPasswordReset = async (email) => {
    const response = await API.post("/auth/password-reset/request", { email });
    return response.data;
};

export const confirmPasswordReset = async (resetToken, newPassword) => {
    const response = await API.post("/auth/password-reset/confirm", {
        reset_token: resetToken,
        new_password: newPassword,
    });
    return response.data;
};

export const getProgress = async () => {
    const response = await API.get("/progress");
    return response.data;
};

export default API;