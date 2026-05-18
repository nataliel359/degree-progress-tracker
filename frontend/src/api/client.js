import axios from "axios";

const API = axios.create({
    baseURL: "http://127.0.0.1:8000"
});

export const getProgress = async () => {
    const response = await API.get("/progress");
    return response.data;
};